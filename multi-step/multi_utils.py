import re
import pandas as pd
import json
import string
from typing import Dict, List, Tuple, Optional, Any
"""
this script is usedby bothscripts in defining functions that are commonly shared
"""

#Similar to devin's function, if it's already a dict leave it, otherwise load from JSON string
def parse_spec(spec_str: str) -> Dict:
    """Parse spec string into dictionary."""
    if pd.isna(spec_str) or spec_str == '':
        return {}
    
    if isinstance(spec_str, dict):
        return spec_str
    
    try:
        return json.loads(spec_str)
    except:
        return {}


def load_combined_data(file_path: str = 'combined_input.csv') -> pd.DataFrame:

    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return pd.DataFrame()

def normalize_template(template: str) -> str:
    normalized = template.translate(str.maketrans('', '', string.punctuation))
    normalized = ' '.join(normalized.split())
    return normalized.lower()

def get_similar_templates(target_template: str, available_templates: set, threshold: float = 0.7) -> list:
    target_norm = normalize_template(target_template)
    matches = []
    
    for available in available_templates:
        available_norm = normalize_template(available)
        if target_norm == available_norm:
            matches.append((available, 1.0))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return [match[0] for match in matches]
def generate_template_pairs(df, link_template, start_matches, end_matches, max_samples_per_group, pairs_list):
    pairs_found = 0
    
    for start_template in start_matches[:3]:  
        for end_template in end_matches[:3]:
            if start_template == end_template:
                continue  
                
            left_matches = df[df['query_template'] == start_template].copy()
            right_matches = df[df['query_template'] == end_template].copy()
            
            if not left_matches.empty and not right_matches.empty:
                pairs_found += process_direction_pairs(
                    left_matches, right_matches, link_template, max_samples_per_group, pairs_list,
                    start_template, end_template
                )
    
    return pairs_found

def process_direction_pairs(left_matches, right_matches, link_template, max_samples_per_group, 
                          pairs_list, start_template, end_template):
    left_matches['orig_idx'] = left_matches.index
    right_matches['orig_idx'] = right_matches.index
    
    left_sample = left_matches.head(max_samples_per_group)
    right_sample = right_matches.head(max_samples_per_group)
    
    left_sample['_join_key'] = 1
    right_sample['_join_key'] = 1

    merged = left_sample.merge(right_sample, on='_join_key', suffixes=('_1', '_2'))
    merged = merged.drop('_join_key', axis=1)
    
    
    sample_size = min(max_samples_per_group, len(merged))
    if sample_size > 0:
        truncated = merged.head(sample_size)
        
        enriched_link = link_template.copy()
        enriched_link['_matched_start'] = start_template
        enriched_link['_matched_end'] = end_template
        
        for i1, i2 in zip(truncated['orig_idx_1'], truncated['orig_idx_2']):
            pairs_list.append((int(i1), int(i2), enriched_link.copy()))
        
        return sample_size
    
    return 0
def add_dataframe_columns(row_dict, d1, d2, df):
    for col in df.columns:
        if col != 'orig_idx':  
            row_dict[f"D1_{col}"] = d1.get(col, '')
            row_dict[f"D2_{col}"] = d2.get(col, '')


#Extract dataset schema- exact same as devin's functions
def get_dataset_schema(d1, d2, fallback_id):
    dataset_schema = ""
    if pd.notna(d1.get('dataset_schema', '')):
        dataset_schema = d1.get('dataset_schema', '')
    elif pd.notna(d2.get('dataset_schema', '')):
        dataset_schema = d2.get('dataset_schema', '')
    else:
        solution_d1 = str(d1.get('solution', ''))
        solution_d2 = str(d2.get('solution', ''))
        if 'sample' in solution_d1.lower():
            match = re.search(r"'sample':\s*'([^']+)'", solution_d1)
            if match:
                dataset_schema = match.group(1)
        elif 'sample' in solution_d2.lower():
            match = re.search(r"'sample':\s*'([^']+)'", solution_d2)
            if match:
                dataset_schema = match.group(1)
        else:
            dataset_schema = f"Dataset_{fallback_id}"
    
    return dataset_schema

#creating specs for pairs
def create_combined_spec_fixed(d1_spec: dict, d2_spec: dict, link_template: dict) -> dict:
    transition_type = link_template.get('transition_type', '')
    transition_subtype = link_template.get('transition_subtype', '')
    
    if transition_type == 'comparative change':
        return generate_comparative_spec(d1_spec, d2_spec, link_template)
    elif transition_type == 'overlay':
        return generate_overlay_spec(d1_spec, d2_spec, link_template)
    elif transition_type == 'visual change':
        return generate_visual_change_spec(d1_spec, d2_spec, link_template)
    elif transition_type == 'data stratification':
        return apply_data_stratification(d2_spec, link_template)
    elif transition_type == 'scope specificity':
        return generate_scope_specificity_spec(d1_spec, d2_spec, link_template)


def generate_comparative_spec(d1_spec: dict, d2_spec: dict, link_template: dict) -> dict:
    tracks = []
    
    if d1_spec:
        if 'tracks' in d1_spec:
            tracks.extend(d1_spec['tracks'])
        elif 'views' in d1_spec:
            for view in d1_spec['views']:
                if 'tracks' in view:
                    tracks.extend(view['tracks'])
        elif any(key in d1_spec for key in ['data', 'mark', 'x', 'y', 'color']):
            tracks.append(d1_spec)
    
    if d2_spec:
        if 'tracks' in d2_spec:
            tracks.extend(d2_spec['tracks'])
        elif 'views' in d2_spec:
            for view in d2_spec['views']:
                if 'tracks' in view:
                    tracks.extend(view['tracks'])
        elif any(key in d2_spec for key in ['data', 'mark', 'x', 'y', 'color']):
            tracks.append(d2_spec)
    
    combined_spec = {
        "views": [{
            "tracks": tracks
        }]
    }
    
    if d1_spec and 'title' in d1_spec:
        combined_spec["title"] = d1_spec['title']
    elif d2_spec and 'title' in d2_spec:
        combined_spec["title"] = d2_spec['title']
    
    return combined_spec

def generate_overlay_spec(d1_spec: dict, d2_spec: dict, link_template: dict) -> dict:
    tracks = []
    
    if d1_spec:
        if 'tracks' in d1_spec:
            tracks.extend(d1_spec['tracks'])
        elif 'views' in d1_spec:
            for view in d1_spec['views']:
                if 'tracks' in view:
                    tracks.extend(view['tracks'])
        elif any(key in d1_spec for key in ['data', 'mark', 'x', 'y', 'color']):
            tracks.append(d1_spec)
    
    if d2_spec:
        if 'tracks' in d2_spec:
            tracks.extend(d2_spec['tracks'])
        elif 'views' in d2_spec:
            for view in d2_spec['views']:
                if 'tracks' in view:
                    tracks.extend(view['tracks'])
        elif any(key in d2_spec for key in ['data', 'mark', 'x', 'y', 'color']):
            tracks.append(d2_spec)
    
    combined_spec = {
        "layout": "linear",
        "arrangement": "vertical", 
        "views": [{
            "alignment": "overlay",
            "tracks": tracks
        }]
    }
    
    return combined_spec

def generate_visual_change_spec(d1_spec: dict, d2_spec: dict, link_template: dict) -> dict:
    transition_subtype = link_template.get('transition_subtype', '')
    
    if transition_subtype == 'detail view':
        brush_track = d2_spec['tracks']
        
        if 'views' in d1_spec:
            first_view = d1_spec[0]
            mark = first_view['tracks'][0]['mark']
            first_view['tracks']['alignment'] = 'overlay'
            first_view['tracks']['tracks'] = [
                {"mark": mark},
                {
                    "mark": "brush",
                    "x": {"linkingId": "detail-1"},
                    "color": {"value": "blue"}
                }
            ]
            
            combined_spec = {
                "views":[
                    first_view,
                    brush_track
                ]
            }
          
        else:
            first_view = d1_spec['tracks'][0]
            
            mark = first_view['mark']
            first_view['alignment'] = 'overlay'
            first_view['tracks'] = [
                {"mark": mark},
                {
                    "mark": "brush",
                    "x": {"linkingId": "detail-1"},
                    "color": {"value": "blue"}
                }
            ]
            
            combined_spec = {
                "views":[
                    [first_view],
                    brush_track
                ]
            }
            
    else:
    
        if d2_spec:
            if 'views' in d2_spec:
                combined_spec = d2_spec.copy()
            else:
                tracks = []
                if any(key in d2_spec for key in ['data', 'mark', 'x', 'y', 'color']):
                    tracks.append(d2_spec)
                combined_spec = {
                    "views": [{
                        "tracks": tracks
                    }]
                }
        else:
            combined_spec = {"views": [{"tracks": []}]}
        
        if transition_subtype == 'linear':
            combined_spec["layout"] = "linear"
            combined_spec["centerRadius"] = 0.3 #just a test
        elif transition_subtype == 'circular':
            combined_spec["layout"] = "linear"
            
    #elif transition_subtype == 'styling':
    #    pass
    
    if d1_spec and 'title' in d1_spec:
        combined_spec["title"] = d1_spec['title']
    
    return combined_spec

def apply_data_stratification(d2_spec: dict, link_template: dict) -> dict:
    if not d2_spec:
        return {"views": [{"tracks": []}]}
    
    if 'views' in d2_spec:
        combined_spec = d2_spec.copy()
        return combined_spec
    elif 'tracks' in d2_spec:
        return {
            "views": [{
                "tracks": d2_spec['tracks'],
            }]
        }
    elif any(key in d2_spec for key in ['data', 'mark', 'x', 'y', 'color']):
        return {
            "views": [{
                "tracks": [d2_spec],
            }]
        }
    else:
        return {"views": [{"tracks": []}]}

def generate_scope_specificity_spec(d1_spec:dict, d2_spec: dict, link_template: dict) -> dict:
    
    if 'views' in d1_spec:
        # find any domain specs and change
        for track in d1_spec['views']['tracks']:
            if 'x' in track:
                track['x']['domain'] = d2_spec
                
    else:
        for track in d1_spec['tracks']:
            if 'x' in track:
                
                track['x']['domain'] = d2_spec
    
    return d1_spec