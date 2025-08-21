#pair running
import pandas as pd
import json
import sys
from typing import Dict, List, Tuple
from multi_utils import (parse_spec, get_similar_templates, load_combined_data, get_dataset_schema, generate_template_pairs,add_dataframe_columns, create_combined_spec_fixed
)

def process_pairs(
    df: pd.DataFrame,
    pairs: List[Dict],
    max_samples_per_group
) -> List[Tuple[int, int, Dict]]:
    linked_pairs = []
    
    df_templates = set(df['query_template'].unique()) if 'query_template' in df.columns else set()
    
    for i, pair in enumerate(pairs):
        template = pair["template"]
        start_q = template["start"].strip()
        end_q = template["end"].strip()
        transition_type = pair.get('transition_type', 'unknown')
        transition_subtype = pair.get('transition_subtype', '')
        
        start_matches = get_similar_templates(start_q, df_templates, threshold=0.7)
        end_matches = get_similar_templates(end_q, df_templates, threshold=0.7)
    
        
        pair['_is_pair'] = True
        
        pairs_found = generate_template_pairs(
            df, pair, start_matches, end_matches, max_samples_per_group, linked_pairs
        )
        
        if pairs_found == True:
            print(f"Found {pairs_found} pairs for this template")
    
    #add stats later
    return linked_pairs

def export_pairs_to_csv(
    df: pd.DataFrame,
    linked_pairs: List[Tuple[int, int, Dict]],
    output_path
) -> pd.DataFrame:
    
    
    pairs_records = []
    
    for pair_idx, (idx1, idx2, link_template) in enumerate(linked_pairs):
        d1 = df.iloc[idx1]
        d2 = df.iloc[idx2]
        
        d1_spec = parse_spec(d1.get('spec', ''))
        d2_spec = parse_spec(d2.get('spec', ''))
        combined_spec = create_combined_spec_fixed(d1_spec, d2_spec, link_template)
        
        dataset_schema = get_dataset_schema(d1, d2, pair_idx)
        
        row_dict = {
            'conversation_id': pair_idx,  #this already increments correctly for pairs
            #'matched_start': link_template.get('_matched_start', ''), debug statementss to see if its same question but off by punctuation
            #'matched_end': link_template.get('_matched_end', ''),
            'transition_type': link_template['transition_type'],
            'dataset_schema': dataset_schema,
            'combined_spec': json.dumps(combined_spec)
        }
        
        add_dataframe_columns(row_dict, d1, d2, df)
        pairs_records.append(row_dict)
    
    pairs_df = pd.DataFrame(pairs_records)
    pairs_df.to_csv("Linked_pairs.csv", index=False)    
    return pairs_df

if __name__ == "__main__":
    df = load_combined_data()
    with open("pairs.json", 'r') as f:
        pairs = json.load(f)
    
    
    max_pairs = 1000 #change this if you wanna change number of pairs
    linked_pairs = process_pairs(df, pairs, max_pairs)
    
    pairs_df = export_pairs_to_csv(df, linked_pairs)
    print("built pairs")