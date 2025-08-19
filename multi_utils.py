import re
import pandas as pd
import json
from typing import Dict, List, Tuple, Optional, Any
from difflib import SequenceMatcher
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


#def load_combined_data(file_path: str = 'combined_input.csv') -> pd.DataFrame:
def load_combined_data(file_path: str = 'basic-addition.csv') -> pd.DataFrame:

    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please run combine_data_sources.py first.")
        return pd.DataFrame()

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
        
        if transition_subtype == 'layout_change':
            combined_spec["layout"] = "circular"
            combined_spec["centerRadius"] = 0.3 #just a test
            
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
        if 'views' in combined_spec and combined_spec['views']:
            combined_spec['views'][0]['stratified'] = True
        return combined_spec
    elif 'tracks' in d2_spec:
        return {
            "views": [{
                "tracks": d2_spec['tracks'],
                "stratified": True
            }]
        }
    elif any(key in d2_spec for key in ['data', 'mark', 'x', 'y', 'color']):
        return {
            "views": [{
                "tracks": [d2_spec],
                "stratified": True
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