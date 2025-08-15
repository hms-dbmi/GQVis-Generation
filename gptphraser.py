import time
import pickle
import sys
import re
from typing import Dict, Optional, Tuple
import pandas as pd
import os
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import json
from dotenv import load_dotenv
from rich import print
load_dotenv()

CACHE_FILE = "./datasets/paraphrase_cache.pkl"

def load_schema(schema_files):
    schema_list = []
    for file in schema_files:
        with open(file, "r") as f:
            loaded_schemas = json.load(f)
            if isinstance(loaded_schemas, list):
                schema_list.extend(loaded_schemas)
            else:
                schema_list.append(loaded_schemas)
    return flatten_schema_list(schema_list)

def paraphrase(df, schema_list, only_cached: Optional[bool] = False) -> pd.DataFrame:
    '''
    Input dataframe will have the following relevant columnns:
    - query_base: the original query
    - dataset_schema: the name of the dataset schema
    
    Output dataframe will have the following relevant columns:
    - query: the paraphrased query
    - expertise: the expertise score of the paraphrased query
    - formality: the formality score of the paraphrased query
    '''
    # simplify the schema_list by removing long attributes that aren't needed in the prompt
    schema_list = [json.loads(json.dumps(schema)) for schema in schema_list]
    for dataset_schema in schema_list:
        resources = dataset_schema.get("resources", [])
        if not isinstance(resources, list):
            raise ValueError(f"Expected a list of resources, but got {type(resources)}")
        for resource in resources:
            resource_schema = resource.get("schema", {})
            if not isinstance(resource_schema, dict):
                raise ValueError(f"Expected a dict for schema, but got {type(resource_schema)}")
            

    cache = get_cache()
    index = 0
    llm = init_llm()
    cache_interval = 25
    interval_index = 0

    lock = threading.Lock()
    completed_rows = 0

    max_worker_count = 5

    def worker(row, row_index):
        nonlocal interval_index, completed_rows
        query_base = row["query_base"]
        dataset_name = row["dataset_schema"]
        dataset_schema = next((schema for schema in schema_list if schema.get('udi:name', schema.get('name')) == dataset_name), None)
        # convert nexted dict into json string
        if dataset_schema is not None:
            dataset_schema = dataset_schema.get("name", "")
        else:
            raise ValueError(f"Dataset schema '{dataset_name}' not found in schema list.")
        try:
            key = f"{dataset_name}¶{query_base}"
            response, is_cached = paraphrase_query(lock, llm, key, query_base, dataset_schema, cache, only_cached)
        except Exception as e:
            print(f"Error in row {row_index}: {e}")
            time.sleep(5)
            return [], row_index
            
        if not is_cached and not only_cached:
            time.sleep(1.5)
        result_rows = []
        if response:
            for sentence in response.sentences:
                new_data = {
                    "query": sentence.paraphrasedSentence,
                    "expertise": sentence.expertise,
                    "formality": sentence.formality,
                }
                new_data.update(row)
                result_rows.append(new_data)
        with lock:
            try:
                completed_rows += 1
                display_progress(df, completed_rows)
            except Exception as e:
                print(f"Error updating progress: {e}")
        if not is_cached:
            with lock:
                try:
                    interval_index += 1
                    if interval_index % cache_interval == 0:
                        update_cache(cache)
                except Exception as e:
                    print(f"Error updating cache file: {e}")
        return result_rows, row_index


    total_rows = len(df)
    new_rows = [None] * total_rows

    with ThreadPoolExecutor(max_workers=max_worker_count) as executor:
        futures = {executor.submit(worker, row, idx): idx for idx, (_, row) in enumerate(df.iterrows())}

        for future in as_completed(futures):
            try:
                result_rows, index = future.result(timeout=90)
            except Exception as e:
                print(f"Timeout or error in future {futures[future]}: {e}")
                continue
            with lock:
                try:
                    new_rows[index] = result_rows
                except Exception as e:
                    print(f"Error updating new_rows list: {e}")

    # Flatten the list of lists
    new_rows = [item for sublist in new_rows if sublist is not None for item in sublist]

    update_cache(cache)
    df = pd.DataFrame(new_rows)
    return df

def display_progress(df, index):
    total_rows = len(df)
    progress = (index / total_rows) * 100
    bar_length = 30
    filled_length = int(bar_length * index // total_rows)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f"\rParaphrasing row {index}/{total_rows} [{bar}] {progress:.2f}%")
    sys.stdout.flush()

def get_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "rb") as f:
                cache = pickle.load(f)
        except Exception as e:
            print(f"Failed to load cache from file: {e}")
    return cache

def update_cache(cache):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)
    return


class ParaphrasedSentence(BaseModel):
    """A paraphrased sentence with metadata on the dimension of formality and expertise"""

    paraphrasedSentence: str = Field(description="The paraphrased sentence.")
    formality: int = Field(
        description="Colloquial (Score=1) language is informal and used in everyday conversation, while standard language (Score=5) follows established rules and conventions and is used in more formal situations."
    )
    expertise: int = Field(
        description="Technical language (Score=5) is often used by experts in a particular field and includes specialized terminology and jargon. Non-technical language (Score=1), on the other hand, is more accessible to a general audience and avoids the use of complex terms."
    )

class ParaphrasedSentencesList(BaseModel):
    """A class that contains a list of paraphrased sentences."""
    sentences: list[ParaphrasedSentence] = Field(
        default_factory=list,
        description="A list of paraphrased sentences with their metadata."
    )

def construct_prompt_template():
    return '''
You are a paraphrasing assistant. Your task is to rewrite a given sentence with various styles of language usage.
The sentence will either be a question about genomics data, or request to construct a genomics data visualization. You must produce different paraphrased versions of the sentence.

The input sentence will include entity, sample, and location from the data.
The dataset schema will also be provided to you to enable better paraphrasing these names.
More technical language may use the exact field names, while more colloquial language may use more general terms, synonyms, and will likely not use the exact field names. All questions should be answered by a genomics data visualization in 2D.

E.g, Where do structural variants (SVs) fall in relation to the FBXW7 gene?

Each paraphrase corresponds to a unique pair of:
- Score-A (formality): 1 (very colloquial) to 5 (very formal)
- Score-B (expertise): 1 (non-technical) to 5 (very technical)

Use this format:
Score-A <A>, Score-B <B>: <Paraphrased sentence>

Input:
Sentence: {sentence}
Dataset schema: {dataset_schema}

Output:
(Write 10 paraphrased sentences, one for each of the following pairs: (1,1), (1,5), (3,1), (3,5), (5,1), (5,5), (2,3), (3,2), (4,4), (2,5), using the format above.)
'''

def init_llm():

    llm = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORG_ID"),
        #model_kwargs= {"project": os.environ.get("OPENAI_PROJECT_ID")}
    )

    prompt_template = PromptTemplate.from_template(construct_prompt_template())

    llm_chained = prompt_template | llm
    return llm_chained


def paraphrase_query(cache_lock, llm, key, query: str, dataset_schema: str, cache: Dict[str, 'ParaphrasedSentencesList'] = {}, only_cached = False) -> Tuple['ParaphrasedSentencesList', bool]:
    if key in cache:
        return cache[key], True
    if only_cached:
        not_paraphrased = ParaphrasedSentence(
            paraphrasedSentence=query,
            formality=-1,
            expertise=-1
        )
        response = ParaphrasedSentencesList(
            sentences=[not_paraphrased]
        )
        return response, True

    # repeat the paraphrasing 10 times for each input
    sentences = []
    for _ in range(10):
        output = llm.invoke({
            "sentence": query,
            "dataset_schema": dataset_schema,
            "dim1_1": "Colloquial",
            "dim1_5": "Standard",
            "dim2_1": "Non-technical",
            "dim2_5": "Technical"
        })
        try:
            output_str = str(output)
            for line in output_str.split("\n"):
                match = re.match(r"Score-A\s*(\d),\s*Score-B\s*(\d):\s*(.+)", line.strip())
                if match:
                    a_score, b_score, sentence = match.groups()
                    sentences.append(ParaphrasedSentence(
                        paraphrasedSentence=sentence.strip(),
                        formality=int(a_score),
                        expertise=int(b_score)
                    ))
        except Exception as e:
            print(f"Error parsing GPT output: {e}")

    #filter to only the 10 expected pairs, first occurrence only
    expected_pairs = [(1,1), (1,5), (3,1), (3,5), (5,1), (5,5), (2,3), (3,2), (4,4), (2,5)]
    filtered_sentences = []
    seen_pairs = set()
    for s in sentences:
        pair = (s.formality, s.expertise)
        if pair in expected_pairs and pair not in seen_pairs:
            filtered_sentences.append(s)
            seen_pairs.add(pair)
        if len(filtered_sentences) == 10:
            break

    response = ParaphrasedSentencesList(sentences=filtered_sentences)
    with cache_lock:
        try:
            cache[key] = response
        except Exception as e:
            print(f"Error updating cache object: {e}")
    return response, False


def flatten_schema_list(schema_list):
    flattened = []
    for item in schema_list:
        if isinstance(item, list):
            flattened.extend(flatten_schema_list(item))  
        elif isinstance(item, dict):
            flattened.append(item)
        else:
           raise ValueError(f"Unexpected item in schema list: {type(item)}")
    return flattened

if __name__ == "__main__":
    schema_files = ["all-schema.json"]  
    schema_list = load_schema(schema_files)
    for i, schema in enumerate(schema_list):
        if not isinstance(schema, dict):
            raise ValueError(f"Schema at index {i} is not a dictionary: {type(schema)}")

    df = pd.read_csv("test.csv")  
    result_df = paraphrase(df, schema_list, only_cached=False)

    result_df.to_csv("testresult.csv", index=False)
    print(result_df.head())