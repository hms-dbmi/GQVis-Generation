import time
import pickle
import sys
import re
import pandas as pd
import os
import json
from typing import Dict, Optional, Tuple, List, Any
from enum import Enum
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dotenv import load_dotenv
from rich import print
load_dotenv()

CACHE_FILE = "./datasets/paraphrase_cache.pkl"

#class to store transition types -> extensible for future types

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

def parse_solution(sol):
    """Parse solution field from JSON string or dict"""
    if isinstance(sol, dict):
        return sol
    try:
        return json.loads(sol)
    except (TypeError, ValueError):
        from ast import literal_eval
        try:
            return literal_eval(sol)
        except:
            return {}

def verify_entity_match(start_template: str, end_template: str, match_config: List[Dict[str, Any]], solution: Dict[str, Any]) -> bool:
    """
    Verify that entity placeholders match according to the match configuration.
    This ensures entity consistency without using regex.
    """
    if not match_config:
        return True  # No match requirements
    
    for match_rule in match_config:
        start_placeholder = match_rule.get("start")
        end_placeholder = match_rule.get("end") 
        match_type = match_rule.get("on")
        
        if match_type == "entity":
            # Extract entity from solution data
            # For now, we'll do a simple string replacement check
            # This logic can be enhanced based on your specific needs
            if start_placeholder in start_template and end_placeholder in end_template:
                continue  # Basic match validation passed
            else:
                return False
    
    return True

#follow linked pairs similar logic as Devin's code
def build_linked_pairs_from_csv(
    df: pd.DataFrame,
    link_templates: List[Dict[str, Any]]
) -> List[Tuple[int, int, Dict[str, Any]]]:

    linked_pairs: List[Tuple[int, int, Dict[str, Any]]] = []
    
    for L in link_templates:
        start_template = L['template']['start']
        end_template = L['template']['end']  
        match_config = L.get('match', [])
        
        for idx, row in df.iterrows():
            # Handle slight variations in template matching (e.g., with/without question marks)
            row_template = row['query_template'].strip()
            start_template_clean = start_template.strip()
            
            # Remove trailing punctuation for matching
            if row_template.rstrip('?') == start_template_clean.rstrip('?'):
                solution = parse_solution(row.get('solution', '{}'))
                
                # Verify entity match if match configuration exists
                if verify_entity_match(start_template, end_template, match_config, solution):
                    followup_question = end_template

                    pair_info = L.copy()
                    pair_info['followup_question'] = followup_question
                    linked_pairs.append((int(idx), int(idx), pair_info))
    
    print(f"Created {len(linked_pairs)} linked pairs")
    return linked_pairs

def replace_placeholders_in_template(template_string: str, solution_data: dict) -> str:
    """
    Replace placeholders in template with actual values from solution data.
    Uses simple string replacement to avoid regex.
    """
    result = template_string
    
    # Handle sample placeholders <S>
    if '<S>' in result and 'S' in solution_data:
        sample_name = solution_data['S'].get('sample', 'sample')
        result = result.replace('<S>', sample_name)
    
    # Handle entity placeholders <E>, <E1>, <E2>
    if '<E>' in result and 'S.E' in solution_data:
        entity_name = solution_data['S.E'].get('name', 'entity')
        result = result.replace('<E>', entity_name)
    
    if '<E1>' in result and 'S.E1' in solution_data:
        entity1_name = solution_data['S.E1'].get('name', 'entity1')
        result = result.replace('<E1>', entity1_name)
    
    if '<E2>' in result and 'S.E2' in solution_data:
        entity2_name = solution_data['S.E2'].get('name', 'entity2')
        result = result.replace('<E2>', entity2_name)
    
    # Handle location placeholders <L>
    if '<L>' in result and 'S.L' in solution_data:
        location_name = solution_data['S.L'].get('gene', 'location')
        result = result.replace('<L>', location_name)
    
    return result

def get_entity_mapping_from_solution(solution_data: dict, template_match_rules: list) -> dict:
    """
    Create entity mapping based on template match rules and solution data.
    Returns mapping of placeholder names to actual entity values.
    """
    mapping = {}
    
    # Extract available entities from solution data
    entities = {}
    if 'S.E' in solution_data:
        entities['E'] = solution_data['S.E']
    if 'S.E1' in solution_data:
        entities['E1'] = solution_data['S.E1']
    if 'S.E2' in solution_data:
        entities['E2'] = solution_data['S.E2']
    
    # Apply match rules if they exist
    if template_match_rules:
        for rule in template_match_rules:
            start_placeholder = rule.get('start')
            end_placeholder = rule.get('end')
            match_type = rule.get('on')
            
            if match_type == 'entity' and start_placeholder in entities:
                # Map end placeholder to same entity as start
                mapping[end_placeholder] = entities[start_placeholder]
                mapping[start_placeholder] = entities[start_placeholder]
    
    # Fill in any missing mappings with available entities
    for placeholder, entity_data in entities.items():
        if placeholder not in mapping:
            mapping[placeholder] = entity_data
    
    return mapping

def export_template_pairs_to_csv(
    df: pd.DataFrame,
    linked: list[tuple[int, int, dict]],
    output_path: str = "template_pairs.csv"
):
    records = []
    for idx1, idx2, L in linked:
        d1 = df.loc[idx1]
        d2 = df.loc[idx2]
        row_dict = {
            "template_start": L["template"]["start"],
            "template_end":   L["template"]["end"],
        }
        
        # Parse solution data to extract entities and sample info
        d1_solution = eval(d1['solution']) if isinstance(d1['solution'], str) else d1['solution']
        d2_solution = eval(d2['solution']) if isinstance(d2['solution'], str) else d2['solution']
        
        # Replace placeholders in D1_query_base using template start and D1 solution
        d1_template_filled = replace_placeholders_in_template(L["template"]["start"], d1_solution)
        row_dict["D1_query_base"] = d1_template_filled
        
        row_dict["D1_dataset_schema"] = d1['dataset_schema']
        row_dict["D2_dataset_schema"] = d2['dataset_schema']


        # Extract transition subtype from the link template or solution
        transition_subtype = L.get("transition_subtype")
        row_dict["transition_subtype"] = transition_subtype
    
        for col in df.columns:
            if col not in ['query_base', 'dataset_schema']:
                row_dict[f"D1_{col}"] = d1[col]
        
        # Get match rules for entity mapping
        match_rules = L.get("match", [])
        
        if L.get("transition_type") == "comparative addition": 
            # For comparative addition, D2 typically uses same entities as D1
            d2_template_filled = replace_placeholders_in_template(L["template"]["end"], d1_solution)
            row_dict["D2_query_base"] = d2_template_filled
            row_dict["D2_query_template"] = L["template"]["end"]  
            row_dict["D2_constraints"] = f"[\"E2['format'] == ''\""


            row_dict["D2_spec_template"] = L.get("spec")

            row_dict["D2_query_type"] = "utterance"

            row_dict["D2_creation_method"] = "template_expansion"
            row_dict["D2_chart_type"] = "comparative addition"
        elif L.get("transition_type") == "visual change":
            # For visual change, apply match rules to determine entity mapping
            # if match_rules:
            #     # Create entity mapping based on match rules
            #     entity_mapping = get_entity_mapping_from_solution(d1_solution, match_rules)
            #     # Use D1 solution but apply entity mapping as needed
            #     solution_for_d2 = d1_solution.copy()
            #     d2_template_filled = replace_placeholders_in_template(L["template"]["end"], solution_for_d2)
            # else:
            d2_template_filled = replace_placeholders_in_template(L["template"]["end"], d1_solution)
            
            row_dict["D2_query_base"] = d2_template_filled
            row_dict["D2_query_template"] = L["template"]["end"]
            row_dict["D2_constraints"] = "[]"  #no specific constraints for visual changes
            row_dict["D2_spec_template"] = L.get("spec")
            row_dict["D2_query_type"] = "utterance"
            row_dict["D2_creation_method"] = "template_expansion"
            row_dict["D2_chart_type"] = "visual_change"
        elif L.get("transition_type") == "overlay":
            # For overlay, use D2 solution to get different entities
            d2_template_filled = replace_placeholders_in_template(L["template"]["end"], d2_solution)
            row_dict["D2_query_base"] = d2_template_filled

            row_dict["D2_query_template"] = L["template"]["end"]
            row_dict["D2_constraints"] = "[]" #
            row_dict["D2_spec_template"] = L.get("spec")
            row_dict["D2_query_type"] = "utterance"
            row_dict["D2_creation_method"] = "template_expansion"
            row_dict["D2_chart_type"] = "overlay"
        elif L.get("transition_type") == "data stratification":
            # For data stratification, use same solution as D1
            d2_template_filled = replace_placeholders_in_template(L["template"]["end"], d1_solution)
            row_dict["D2_query_base"] = d2_template_filled

            row_dict["D2_query_template"] = L["template"]["end"]
            row_dict["D2_constraints"] = "[]" #no specific constraints for strat
            row_dict["D2_spec_template"] = L.get("spec")
            row_dict["D2_query_type"] = "utterance"
            row_dict["D2_creation_method"] = "template_expansion"
            row_dict["D2_chart_type"] = "data stratification"

        elif L.get("transition_type") == "scope specificity":
            # For scope specificity, use same solution as D1 
            d2_template_filled = replace_placeholders_in_template(L["template"]["end"], d1_solution)
            row_dict["D2_query_base"] = d2_template_filled


            row_dict["D2_query_template"] = L["template"]["end"]
            row_dict["D2_constraints"] = "[]" 

            row_dict["D2_spec_template"] = L.get("spec")

            row_dict["D2_query_type"] = "utterance"

            row_dict["D2_creation_method"] = "template_expansion"
            row_dict["D2_chart_type"] = "scope specificity"
        #the if else ladder would extend to different types of transitions

        d1_complexity = d1.get('chart_complexity', 'medium') #complexity can be changed for others
        complexity_map = {'low': 'medium', 'medium': 'high', 'high': 'high'}
        row_dict["D2_chart_complexity"] = complexity_map.get(d1_complexity, 'high') #default setting for now 
        
        same_columns = ['solution', 'spec_key_count']
        for col in same_columns:
            if col in df.columns:
                row_dict[f"D2_{col}"] = d1[col]
                
        records.append(row_dict)
    
    out_df = pd.DataFrame(records)
    out_df.to_csv(output_path, index=False)
    return out_df

class ParaphrasedQuestionPair(BaseModel):
    """A single paraphrased question pair with metadata"""
    paraphrasedQ1: str = Field(description="The paraphrased version of the input Q1, maintaining the same meaning and intent.")
    paraphrasedQ2: str = Field(description="The paraphrased version of the input Q2, maintaining the same meaning and intent.")
    formality: int = Field(
        description="Formality level (1-5): 1=colloquial, 5=formal. Generated randomly for stylistic variation.",
        ge=1, le=5
    )
    expertise: int = Field(
        description="Expertise level (1-5): 1=non-technical, 5=highly technical. Generated randomly for stylistic variation.",
        ge=1, le=5
    )

class ParaphrasedPairsList(BaseModel):
    """A class that contains exactly one paraphrased question pair."""
    pairs: List[ParaphrasedQuestionPair] = Field(
        description="Exactly one paraphrased question pair that maintains the original meaning.",
        min_items=1,
        max_items=1
    )

def construct_paraphrase_prompt_template(): #currently latches onto the word mapping but we can fix with template generation or rewording question
    template = '''
You are tasked with paraphrasing two specific questions while maintaining their original meaning and intent.

Input Questions:
Q1 (Initial Question): {q_1}
Q2 (Follow-Up Utterance): {q_2}
Transition Type: {transition_type}

Task:
Generate EXACTLY ONE paraphrased version of these two questions. You must:

1. Keep the same core meaning and intent as the original questions
2. Maintain the relationship between Q1 and Q2 
3. Preserve any specific entity names, field names, or data references mentioned
4. Q1 should remain a question requesting a visualization
5. Q2 should remain a follow-up request that builds on Q1

Guidelines:
- Do NOT generate multiple different question pairs
- Do NOT create entirely new questions on different topics
- Do NOT change the fundamental meaning or data focus
- Simply rephrase the language while keeping the same intent
- Generate random formality (1-5) and expertise (1-5) scores for stylistic variation

Return exactly one paraphrased pair that preserves the original meaning.
'''
    return template

def init_llm():
    llm = init_chat_model("gpt-4o", model_provider="openai")
    structured_llm = llm.with_structured_output(ParaphrasedPairsList)
    prompt_template = PromptTemplate.from_template(construct_paraphrase_prompt_template())
    llm_chained = prompt_template | structured_llm
    return llm_chained

def paraphrase_question_pair(
    cache_lock, 
    llm, 
    key, 
    question_1: str, 
    question_2: str, 
    transition_type: str,
    cache: Dict[str, ParaphrasedPairsList] = {}, 
) -> Tuple[ParaphrasedPairsList, bool]:
    
    if key in cache:
        return cache[key], True
    
    
    response = llm.invoke({
        "q_1": question_1,
        "q_2": question_2,
        "transition_type": transition_type,
    })
    
    with cache_lock:
        try:
            cache[key] = response
        except Exception as e:
            print(f"Error updating cache object: {e}")
    
    return response, False

def generate_comparative_addition_spec(
    original_spec: str,
    question_1: str, 
    question_2: str, 
    dataset_schema: str,
    spec_mods: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    
    if spec_mods is None:
        spec_mods = []
        
    original_spec_dict = json.loads(original_spec)
    modified_spec = json.loads(json.dumps(original_spec_dict))  # deep copy

    if "tracks" in modified_spec and isinstance(modified_spec["tracks"], list):
        for track in modified_spec["tracks"]:
            for mod in spec_mods:
                track.update(json.loads(json.dumps(mod)))
    result = {
        "initial_question": question_1,
        "followup_question": question_2,
        "dataset_schema": dataset_schema,
        "spec_template": modified_spec
    }

    return result

def generate_visual_change_spec(
    original_spec: str,
    question_1: str, 
    question_2: str, 
    dataset_schema: str,
    transition_subtype: str,
    spec_mods: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
 
    if spec_mods is None:
        spec_mods = []
        
    original_spec = json.loads(original_spec)
    modified_spec = json.loads(json.dumps(original_spec))  # deep copy

    if transition_subtype == "circular":
        if "tracks" in modified_spec and isinstance(modified_spec["tracks"], list):
            for track in modified_spec["tracks"]:
                for mod in spec_mods:
                    track.update(json.loads(json.dumps(mod)))

    elif transition_subtype == "color":
        if "tracks" in modified_spec and isinstance(modified_spec["tracks"], list):
            for track in modified_spec["tracks"]:
                for mod in spec_mods:
                    track.update(json.loads(json.dumps(mod)))
    result = {
        "initial_question": question_1,
        "followup_question": question_2,
        "dataset_schema": dataset_schema,
        "spec_template": modified_spec
    }
    return result


def generate_overlay_spec(
    original_spec: str,
    question_1: str, 
    question_2: str, 
    dataset_schema: str,
    spec_mods: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate an overlay spec by applying modifications from multi_step_links.json.
    """
    if spec_mods is None:
        spec_mods = []
        
    original_spec_dict = json.loads(original_spec)
    modified_spec = json.loads(json.dumps(original_spec_dict))  # deep copy

    if "tracks" in modified_spec and isinstance(modified_spec["tracks"], list):
        for track in modified_spec["tracks"]:
            for mod in spec_mods:
                track.update(json.loads(json.dumps(mod)))
    result = {
        "initial_question": question_1,
        "followup_question": question_2,
        "dataset_schema": dataset_schema,
        "spec_template": modified_spec
    }
    return result

def generate_data_stratification_spec(
    original_spec: str,
    question_1: str,
    question_2: str,
    dataset_schema: str,
    spec_mods: List[Dict[str, Any]]
) -> Dict[str, Any]:

    original_spec_dict = json.loads(original_spec)
    modified_spec = json.loads(json.dumps(original_spec_dict))
    if "tracks" in modified_spec and isinstance(modified_spec["tracks"], list):
        for track in modified_spec["tracks"]:
            for mod in spec_mods:
                track.update(json.loads(json.dumps(mod)))
    result = {
        "initial_question": question_1,
        "followup_question": question_2,
        "dataset_schema": dataset_schema,
        "spec_template": modified_spec
    }
    return result

def generate_scope_specificity_spec(
    original_spec: str,
    question_1: str, 
    question_2: str, 
    dataset_schema: str,
    spec_mods: List[Dict[str,Any]],
    transition_subtype
) -> Dict[str, Any]:
    
    original_spec_dict = json.loads(original_spec)
    modified_spec = json.loads(json.dumps(original_spec_dict))

    #Case 1: helper function -> view entire genome as a whole! 
    def remove_domain_from_x(track):
        if "x" in track and isinstance(track["x"], dict) and "domain" in track["x"]:
            del track["x"]["domain"]
    
    if transition_subtype == "entirety":
        if "views" in modified_spec and isinstance(modified_spec["views"], list):
            for view in modified_spec["views"]:
                    remove_domain_from_x(view)
        return {
            "initial_question": question_1,
            "followup_question": question_2,
            "dataset_schema": dataset_schema,
            "spec_template": modified_spec
        }

    
    for mod in spec_mods:
        if "title" in mod:
            modified_spec["title"] = mod["title"] #this helps us keep track of where we are changing scope! 

    result = {
        "initial_question": question_1,
        "followup_question": question_2,
        "dataset_schema": dataset_schema,
        "spec_template": modified_spec
    }
    return result


def multi_step_paraphrase_with_specs(
    df: pd.DataFrame, 
    schema_list: List[Dict], 
) -> pd.DataFrame:
    
    cache = get_cache()
    llm = init_llm()
    lock = threading.Lock()
    completed_rows = 0
    max_worker_count = 5

    def worker(row, row_index):
        nonlocal completed_rows
        
        question_1 = row.get("D1_query_base")
        question_2 = row.get("D2_query_base")
        transition_type = row.get("D2_chart_type")  # Changed from transition_type to D2_chart_type
        dataset_name = row.get("D1_dataset_schema")
        original_spec = row.get("D1_spec", "{}")
        solution_str = row.get("D1_solution", "{}")
        
        
        # Check if we have valid questions
        if not question_1 or not question_2:
            with lock:
                completed_rows += 1
                display_progress(df, completed_rows)
            return [], row_index
        
        try:
            solution = eval(solution_str) if isinstance(solution_str, str) else solution_str
        except:
            solution = {}
        
        dataset_schema = next(
            (schema for schema in schema_list 
            if schema.get('udi:name', schema.get('name')) == dataset_name), 
            None
        )
        
        if dataset_schema is None:
            dataset_schema = {"name": dataset_name} 
        
        try:
            key = f"{dataset_name}¶{question_1}¶{question_2}¶{transition_type}"
            response, is_cached = paraphrase_question_pair(
                lock, llm, key, question_1, question_2, transition_type, 
                cache
            )
            
        except Exception as e:
            time.sleep(5)
            return [], row_index
        
        if not is_cached:
            time.sleep(1.5)
        
        result_rows = []
        if response and hasattr(response, 'pairs') and response.pairs:
            for pair_idx, pair in enumerate(response.pairs):
                transition_subtype = row.get("transition_subtype", solution.get("transition_subtype", "default"))
                spec_mods_str = row.get("D2_spec_template", "[]")  # Changed from D2_spec_mods

                if transition_type == "comparative addition":
                    try:
                        spec_mods = json.loads(spec_mods_str) if isinstance(spec_mods_str, str) else spec_mods_str
                    except:
                        spec_mods = []
                    viz_spec_data = generate_comparative_addition_spec(
                        original_spec,
                        pair.paraphrasedQ1, 
                        pair.paraphrasedQ2, 
                        dataset_name,
                        spec_mods
                    )
                elif transition_type == "visual change":
                    try:
                        spec_mods = json.loads(spec_mods_str) if isinstance(spec_mods_str, str) else spec_mods_str
                    except:
                        spec_mods = []
                    viz_spec_data = generate_visual_change_spec(
                        original_spec,
                        pair.paraphrasedQ1, 
                        pair.paraphrasedQ2, 
                        dataset_name,
                        transition_subtype,
                        spec_mods
                    )
                elif transition_type == "overlay":
                    try:
                        spec_mods = json.loads(spec_mods_str) if isinstance(spec_mods_str, str) else spec_mods_str
                    except:
                        spec_mods = []
                    viz_spec_data = generate_overlay_spec(
                        original_spec,
                        pair.paraphrasedQ1, 
                        pair.paraphrasedQ2, 
                        dataset_name,
                        spec_mods
                    )
                elif transition_type == "data stratification":
                    try:
                        spec_mods = json.loads(spec_mods_str) if isinstance(spec_mods_str, str) else spec_mods_str
                    except:
                        spec_mods = []
                    viz_spec_data = generate_data_stratification_spec(
                        original_spec,
                        pair.paraphrasedQ1,
                        pair.paraphrasedQ2,
                        dataset_name,
                        spec_mods
                    )
                elif transition_type == "scope specificity":
                    try:
                        spec_mods = json.loads(spec_mods_str) if isinstance(spec_mods_str, str) else spec_mods_str
                    except:
                        spec_mods = []
                    viz_spec_data = generate_scope_specificity_spec(
                        original_spec,
                        pair.paraphrasedQ1,
                        pair.paraphrasedQ2,
                        dataset_name,
                        spec_mods, 
                        transition_subtype
                    )
                else:
                    print(f"Worker {row_index}: Unknown transition type '{transition_type}', skipping")
                    continue  # Skip unknown transition types
                
                new_data = {
                    "D1_query": pair.paraphrasedQ1,
                    "D2_query": pair.paraphrasedQ2,
                    "expertise": pair.expertise,
                    "formality": pair.formality,
                    "spec": json.dumps(viz_spec_data.get("spec_template", {})),
                    "spec_template": json.dumps(viz_spec_data.get("spec_template", {})),
                }
                new_data.update(row)
                result_rows.append(new_data)
       
        
        with lock:
            completed_rows += 1
            display_progress(df, completed_rows)
        
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
                new_rows[index] = result_rows
                

    new_rows = [item for sublist in new_rows if sublist is not None for item in sublist]
    
    update_cache(cache)
    return pd.DataFrame(new_rows)

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
            cache = {}
    return cache

def update_cache(cache):
    try:
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(cache, f)
    except Exception as e:
        print(f"Failed to save cache: {e}")


if __name__ == "__main__":
    
    with open("multi_step_links.json", "r") as f:
        multi_step_links = json.load(f)
    print(f"Loaded {len(multi_step_links)} link templates")
    
   
    #our current dataset for now -> can be changed to longer .csv 
    df = pd.read_csv("multistepinput.csv")
    print(f"Loaded {len(df)} rows from multistepinput.csv")
    
    #filter to unique "unparaphrased" queries by query_base -> in original script
    if 'query_base' in df.columns:
        df_unique = df.drop_duplicates(subset=['query_base'], keep='first').reset_index(drop=True)
        print(f"After filtering duplicates: {len(df_unique)} unique rows")
    else:
        df_unique = df
        print("No query_base column found, using all rows")
    

    #build linked pairs based on the multi_step_links.json templates
    linked_pairs = build_linked_pairs_from_csv(df_unique, multi_step_links)
    print(f"Generated {len(linked_pairs)} linked pairs")
        
    template_pairs_df = export_template_pairs_to_csv(df_unique, linked_pairs)
    print(f"Exported template pairs: {len(template_pairs_df)} rows")

    with open("example_schema.json", "r") as f:
        schema_list = json.load(f)
    print(f"Loaded {len(schema_list)} schemas")
   

    first_row = template_pairs_df.iloc[0] if len(template_pairs_df) > 0 else None
        
    result_df = multi_step_paraphrase_with_specs(template_pairs_df, schema_list)
    print(f"Generated {len(result_df)} result rows")
        
    if len(result_df) > 0:
        result_df.to_csv("multistepoutput2.csv", index=False)
        print("Results saved to multistepoutput2.csv")
            
    

