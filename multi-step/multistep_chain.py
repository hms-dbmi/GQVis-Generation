#!/usr/bin/env python3
import pandas as pd
import json
import sys
from typing import Dict, List, Tuple
from multi_utils import (
    parse_spec, get_similar_templates,
    load_combined_data, get_dataset_schema, generate_template_pairs, generate_comparative_spec,
    add_dataframe_columns, create_combined_spec_fixed, generate_visual_change_spec
)
#process chains
def load_chain_templates(file_path: str = 'chains.json') -> List[List[Dict]]:
    try:
        with open(file_path, 'r') as f:
            chains = json.load(f)
        print(f"Loaded {len(chains)} chain templates from {file_path}")
        return chains
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return []


def generate_chain_steps(prev_combined_spec: dict, current_d2_spec: dict, link_template: dict) -> dict:
    transition_type = link_template.get('transition_type', '')
    transition_subtype = link_template.get('transition_subtype', '')
    
    #use prev_combined_spec as base and current_d2_spec as the new spec to add
    return create_combined_spec_fixed(prev_combined_spec, current_d2_spec, link_template)

def process_chains(
    df: pd.DataFrame,
    chains: List[List[Dict]],
    max_chains
) -> List[Tuple[int, Dict]]:
    linked_chains = []
    
    df_templates = set(df['query_template'].unique()) if 'query_template' in df.columns else set()
        
    for chain_idx, chain in enumerate(chains):
        
        # 
        # if not chain or not isinstance(chain, list):
        #    
        #     continue
        
        for conversation_index, step in enumerate(chain):
            if 'template' in step:
                start_q = step['template'].get('start', '')
                end_q = step['template'].get('end', '')
                chain_step = step.get('chain_step', conversation_index)
        
        chain_pairs = []
        chain_valid = True
        
        for conversation_index, step_template in enumerate(chain):
            if 'template' not in step_template:
                chain_valid = False
                break
            
            template = step_template["template"]
            start_q = template.get("start", "").strip()
            end_q = template.get("end", "").strip()
            
            if not start_q or not end_q:
                chain_valid = False
                break
            
            start_matches = get_similar_templates(start_q, df_templates, threshold=0.7)
            end_matches = get_similar_templates(end_q, df_templates, threshold=0.7)
            
          
            
            step_template['_chain_id'] = chain_idx
            step_template['_step_in_chain'] = conversation_index
            
            step_pairs = []
            pairs_found = generate_template_pairs(
                df, step_template, start_matches, end_matches, max_chains, step_pairs
            )
            
            if pairs_found == 0:
                chain_valid = False
                break
            else:
                chain_pairs.extend(step_pairs)
        
        if chain_valid and chain_pairs:
            chain_by_steps = {}
            for pair_data in chain_pairs:
                idx1, idx2, link_template = pair_data
                step_in_chain = link_template.get('_step_in_chain', 0)
                if step_in_chain not in chain_by_steps:
                    chain_by_steps[step_in_chain] = []
                chain_by_steps[step_in_chain].append(pair_data)
            
            linked_chains.append((chain_idx, chain_by_steps))
            print(f"chain {chain_idx} with {len(chain_pairs)} total pairs across {len(chain_by_steps)} steps")
        else:
            print(f"failed to build complete chain {chain_idx}")
    
    print(f"linked chains found: {len(linked_chains)}")
    
    return linked_chains

def export_chains(
    df: pd.DataFrame,
    linked_chains: List[Tuple[int, Dict]],
    max_chains_per_template
) -> pd.DataFrame:
    
    if not linked_chains:
        return pd.DataFrame()
    
    chains_records = []
    global_conversation_id = 0
    
    for chain_idx, chain_by_steps in linked_chains:
        step_counts = [len(chain_by_steps[conversation_index]) for conversation_index in sorted(chain_by_steps.keys())]
        min_pairs = min(step_counts) if step_counts else 0
        max_chains_to_generate = min(min_pairs, max_chains_per_template)
        
        print(f"pair counts: {step_counts}")
        print(f"{max_chains_to_generate} complete chains")
        
        for chain_instance in range(max_chains_to_generate):
            conversation_specs = {}
            current_conversation_id = global_conversation_id
            previous_d2_query = None  #track previous D2 query for continuity check
            
            for conversation_index in sorted(chain_by_steps.keys()):
                step_pairs = chain_by_steps[conversation_index]
                
                if chain_instance < len(step_pairs):
                    idx1, idx2, link_template = step_pairs[chain_instance]
                    
                    d1 = df.iloc[idx1]
                    d2 = df.iloc[idx2]
                    
                    d1_spec = parse_spec(d1.get('spec', ''))
                    d2_spec = parse_spec(d2.get('spec', ''))
                    
                    #combine specs based on chain position
                    if conversation_index > 0 and conversation_index - 1 in conversation_specs:
                        prev_combined_spec = conversation_specs[conversation_index - 1]
                        combined_spec = generate_chain_steps(prev_combined_spec, d2_spec, link_template)
                    else:
                        #first step in chain
                        combined_spec = create_combined_spec_fixed(d1_spec, d2_spec, link_template)
                    
                    
                    conversation_specs[conversation_index] = combined_spec
                    
                    #this might need improvement
                    #previous_d2_query = d2.get('query', d2.get('query_base', ''))
                    
                    dataset_schema = get_dataset_schema(d1, d2, chain_idx)
                    
                    row_dict = {
                        'conversation_id': current_conversation_id,
                        'conversation_index': conversation_index,
                        'transition_type': link_template['transition_type'],
                        'dataset_schema': dataset_schema,
                        'combined_spec': json.dumps(combined_spec)
                    }
                    
                    add_dataframe_columns(row_dict, d1, d2, df)
                    chains_records.append(row_dict)
            
            global_conversation_id += 1  
    
    chains_df = pd.DataFrame(chains_records)
    chains_df.to_csv("multistep_chains.csv", index=False)    
    return chains_df


if __name__ == "__main__":
    df = load_combined_data()
    chains = load_chain_templates()
    
    print(f"{len(df)} from combined dataset")
    print(f"{len(chains)} chain templates")

    max_chains_exported = 50 #change this to change # of results

    linked_chains = process_chains(df, chains, max_chains_exported)
    
    chains_df = export_chains(df, linked_chains, max_chains_exported)

