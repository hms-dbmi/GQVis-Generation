import json
import os
import sys
import time
import pickle
from ast import literal_eval
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re
import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from rich import print

from typing import List, Tuple, Dict, Any, Optional
load_dotenv()

CACHE_FILE = "multi-step/multi_step_paraphrase_cache.pkl"

def get_by_path(d: Dict[str, Any], path: str) -> Any:
    """
    Traverse a nested dict `d` following a dot-separated `path` (e.g. "E.F.entity").
    Returns the value or None if any key is missing.
    """
    cur = d
    for key in path.split('.'):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur

# assuming `df` is your DataFrame and df['solution'] contains JSON‐encoded strings
def parse_solution(sol):
    # if it's already a dict, leave it
    if isinstance(sol, dict):
        return sol
    # otherwise, try to load from JSON string
    try:
        return json.loads(sol)
    except (TypeError, ValueError):
        # fallback: if it's a Python‐style dict literal
        from ast import literal_eval
        return literal_eval(sol)


class ParaphrasedSentence(BaseModel):
    """A paraphrased sentence with metadata on the dimension of formality and expertise"""

    paraphrasedQ1: str = Field(description="The paraphrased Q1.")
    paraphrasedQ2: str = Field(description="The paraphrased Q2.")
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
    template = '''
You will be given:
    • Q1 (Initial Question): Pose a clear question that would prompt a genomics visualization. Use language appropriate to the specified Expertise and Formality scores.
	• Q2 (Follow-Up Question): Paraphrase the new insight or metric revealed by that follow-up visualization. Maintain the same Expertise and Formality style as Q1.
	• Expertise Score (1–5): 1 = non-technical → 5 = highly technical
	• Formality Score (1–5): 1 = colloquial → 5 = very formal

Task:
Rewrite Q1 and Q2 as a natural two-step interaction around a data visualization:
	1.	Q1 should clearly request a visualization, using language matching the given Expertise and Formality.
    2.	Q2 should paraphrase a new follow-up utterance after the insights revealed by previous visualization, in the same style.
-----

Guidelines:
- Consistency: Apply the same expertise and formality level to both Q1 and Q2.
- Formality → Field Names: preserve exact field names, but please fill out abbrevations when necesssary- common abbreivations include sv for structural variants, cna for copy number alterations, cnv for copy number variants.
- Expertise → Terminology: use precise, domain-specific terms.
-----
Example:
 
Input:
  Q1: What is the conservative atac peaks data?
  Q2: Add an sv data view.
  
Output:
  Q1: Could you please display the simple atac peaks information?
  Q2: Provide additional sv data to compare. 

-----
Rewrite the following:
Q1: {q_1}
Q2: {q_2}


'''
    # constuct all possible score combinations, like DQVis
    for i in [1, 3, 5]:
        for j in [1, 3, 5]:
            template += f'Expertise Score: {i}, Formality Score: {j}'
    return template

def init_llm():

    llm = ChatOpenAI(
        api_key = os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORG_ID"),
        model="gpt-4o"
    )

    prompt_template = PromptTemplate.from_template(construct_prompt_template())

    llm_chained = prompt_template | llm
    return llm_chained

#in the future we can add dataset_schema1 and dataset_schema2 for added context within multi-step paraphrasing
def paraphrase_query(
        cache_lock, 
        llm, 
        key, 
        question_1: str, 
        question_2: str, 
        dataset_schema1: str, 
        dataset_schema2: str, 
        cache: Dict[str, ParaphrasedSentencesList] = {}, 
        only_cached = False
    ) -> Tuple[ParaphrasedSentencesList, bool]:

    if key in cache:
        return cache[key], True
    
    if only_cached:
        not_paraphrased = ParaphrasedSentence(
            paraphrasedQ1=question_1,
            paraphrasedQ2=question_2,
            formality=-1,
            expertise=-1
        )
        response = ParaphrasedSentencesList(
            sentences=[not_paraphrased]
        )
        return response, True
    
    #get raw text response from LLM
    raw_response = llm.invoke({
        "q_1": question_1,
        "q_2": question_2,
    })
    
    
    output_str = getattr(raw_response, "content", str(raw_response))
    print(f"raw LLM response for debugging: {output_str[:200]}...")
    
    parsed_sentences = []
    
    expertise_formality_sections = re.findall(r"Expertise Score:\s*(\d+),\s*Formality Score:\s*(\d+)", output_str)
    
    if expertise_formality_sections:
        q_pairs = re.findall(r"Q1:\s*(.*?)\s*Q2:\s*(.*?)(?=Expertise Score:|$)", output_str, re.DOTALL)
        
        if len(q_pairs) >= len(expertise_formality_sections):
            for i, (expertise, formality) in enumerate(expertise_formality_sections):
                if i < len(q_pairs):
                    q1 = q_pairs[i][0].strip().strip('*').strip()
                    q2 = q_pairs[i][1].strip().strip('*').strip()
                    
                    parsed_sentences.append(ParaphrasedSentence(
                        paraphrasedQ1=q1,
                        paraphrasedQ2=q2,
                        expertise=int(expertise),
                        formality=int(formality)
                    ))
    #fallback incase LLM does not return structureed response
    if not parsed_sentences:
       
        q1_match = re.search(r"Q1:\s*(.*?)(?=Q2:|$)", output_str, re.DOTALL)
        q2_match = re.search(r"Q2:\s*(.*?)(?=Expertise Score:|$)", output_str, re.DOTALL)
        
        if q1_match and q2_match:
            q1 = q1_match.group(1).strip().strip('*').strip()
            q2 = q2_match.group(1).strip().strip('*').strip()
            
            parsed_sentences.append(ParaphrasedSentence(
                paraphrasedQ1=q1,
                paraphrasedQ2=q2,
                expertise=3,
                formality=3
            ))
    
    response = ParaphrasedSentencesList(sentences=parsed_sentences)
    
    print(f"Extracted {len(parsed_sentences)} paraphrased sentences")
    
    with cache_lock:
        try:
            cache[key] = response
        except Exception as e:
            print(f"Error updating cache object: {e}")
            
    return response, False


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
    # Ensure the directory for the cache file exists
    cache_dir = os.path.dirname(CACHE_FILE)
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)
    return

def display_progress(df, index):
    total_rows = len(df)
    progress = (index / total_rows) * 100
    bar_length = 30
    filled_length = int(bar_length * index // total_rows)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f"\rParaphrasing row {index}/{total_rows} [{bar}] {progress:.2f}%")
    sys.stdout.flush()



def multi_step_paraphrase(df, schema_list, only_cached: Optional[bool] = False) -> pd.DataFrame:
    '''
    Input dataframe will have the following relevant columnns:
    - query_base: the original query
    - dataset_schema: the name of the dataset schema
    
    Output dataframe will have the following relevant columns:
    - query: the paraphrased query
    - expertise: the expertise score of the paraphrased query
    - formality: the formality score of the paraphrased query
    '''
    flattened_schema_list = []
    for item in schema_list:
        if isinstance(item, list):
            for subitem in item:
                if isinstance(subitem, dict):
                    flattened_schema_list.append(json.loads(json.dumps(subitem)))
        elif isinstance(item, dict):
            flattened_schema_list.append(json.loads(json.dumps(item)))
    
    schema_list = flattened_schema_list
    
    
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
        question_1 = row["D1_query_base"]
        question_2 = row["D2_query_base"]
        dataset_name = row["D1_dataset_schema"]
        dataset_name2= row["D2_dataset_schema"]
        dataset_schema1 = next((schema for schema in schema_list if schema['name'] == dataset_name), None)
        dataset_schema2 = next((schema for schema in schema_list if schema['name'] == dataset_name2), None)
        # convert nexted dict into json string
        if dataset_schema1 is not None:
            dataset_schema1 = json.dumps(dataset_schema1, indent=0)
            dataset_schema2 = json.dumps(dataset_schema2, indent=0)
        else:
            raise ValueError(f"Dataset schema '{dataset_name}' not found in schema list.")
        try:
            key = f"{dataset_name}{dataset_name2}{question_1}¶{question_2}"
            response, is_cached = paraphrase_query(
                lock, 
                llm, 
                key, 
                question_1, 
                question_2, 
                dataset_schema1,
                dataset_schema2,
                cache,
                only_cached
            )
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
                    "D1_query": sentence.paraphrasedQ1,
                    "D2_query": sentence.paraphrasedQ2,
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
    #df = df.drop(columns=['D1_query_base', 'D2_query_base'])
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

    #flatten the list of lists
    new_rows = [item for sublist in new_rows if sublist is not None for item in sublist]

    update_cache(cache)
    df = pd.DataFrame(new_rows)
    return df


def print_header(message):
        print("\n" + "#" * 80)
        print("| " + message + " " * (77 - len(message)) + "|")
        print("#" * 80)


if __name__ == "__main__":

    #read the resulting linked_pairs.csv file
    df = pd.read_csv("linked_pairs.csv")
    with open('/Users/arthe/HMS/copy/DQVis-Generation/data-schema/all-schema.json') as f:
        schema_list = json.load(f)
    
    df = multi_step_paraphrase(df=df, schema_list=schema_list)
    paraphrased_question_count = df.shape[0]

    print(f"paraphrased to {paraphrased_question_count:,}.")#amount we reference in paper
    
    df.to_csv('multi_step_pairs.csv', index=False)
