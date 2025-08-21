from typing import List, Dict, Union
import pandas as pd
import re
from constraint import *
import json
import ast
from typing import List, Dict

# from parsimonious.grammar import Grammar
from pprint import pprint

def expand(df, collection):
    expanded_rows=[]
    for _, row in df.iterrows():
        for dataset_schemas in collection: 
            
            all_samples = []
            all_entities = []
            all_fields = []
            all_locations = []
            
            for schema in dataset_schemas: # 1 schema is 1 sample ! --> want list of samples. 
                
                # 1. extract sample metadata
                sample_name=schema['name']
                sample_id = schema['udi:sample-id']
                sample_assembly=schema["udi:assembly"]
                sample_cancer = schema["udi:cancer-type"]
                cell_type = ''
                
                # 2. extract gene data
                schema_genes = schema["udi:genes"]
                gene_list = []
                for elem in schema_genes:
                    gene_list.append({'gene':elem["name"],'start':elem["pos"], 'end':elem['pos'] + 5000, 'chromosome':elem["chr"], })
                    
                # 3. extract data about each file + actual file
                schema_flattened = []
                entity_info=[]
                for file in schema["resources"]:
                    file_name = file["name"] 
                    sample_id = sample_name
                    file_schema = file["schema"]
                    foreignKeys = file_schema.get("foreignKeys", [])
                    file_path = file["path"]
                    
                    for use in file['udi:use']:
                    
                        entity_info.append({
                            'name':file_name,
                            'udi:use':use,
                            'format':file["format"],
                            'position-fields':file["position-fields"],
                            'sample':sample_id,
                            'url': file_path,
                            #'fields': file_schema["fields"],
                            'index-file': file["index-file"]
                        })
                        

                    for col in file_schema["fields"]:
                        schema_flattened.append({
                            "file": file_name,
                            "field": col["name"],  
                            "udi:data_type": col.get("type"),
                            "url": file_path,
                            "foreignKeys": foreignKeys,
                            "column_metadata": col,
                            "sample": sample_id,
                        })

                # 4. Create sample and entity options
                location_options = selectGenes(sample_assembly, gene_list)
                
                sample_options = create_sample_options(schema_flattened, sample_assembly, sample_cancer, location_options)
                entity_options=entity_info                
                
                
                
                # 6. Create field options
                field_options=schema_flattened
                
                all_samples += sample_options
                all_entities += entity_options
                all_fields += field_options
                all_locations += location_options
            
                                        
            new_rows = expand_template(row, all_samples, all_entities, all_fields, all_locations, max_per_template=1500)
            #print(row['taxonomy_type'])
            for new_row in new_rows:
                new_row["dataset_schema"] = sample_name
            expanded_rows.extend(new_rows)
            
            # SAMPLE OPTIONS.  --> entities and fields
            
    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df

def selectGenes(assembly, gene_list, gene_ct=2, chrom_ct=3, popularityWeights=True):
    '''
    select list of genes from assembly. includes the default genes from the listed file 
    in addition to gene_ct - number of default genes. If psopularityWeights = True,
    selection is weighted by gene research popularity.
    '''
    
    sampled_chroms = []
    assembly_num=assembly[-2:]
        
    df = pd.read_csv(f'location_data/refSeq_chromosomes.hg{assembly_num}.tsv', sep='\t')
    chrom_subsample = df.sample(
            n=chrom_ct, 
            replace=False, 
            random_state=42
        )
    
    for row in chrom_subsample.itertuples():
            end = int(row.start + row.length)
            sampled_chroms.append({
                'gene':row.chrom,
                'start': row.start,
                'end': end,
                'chromosome': row.chrom
            })
    
    if len(gene_list) > gene_ct:
        sampled_genes = sampled_chroms + gene_list
        return sampled_genes
    else:
        sampled_genes = []
        df = pd.read_csv(f'location_data/refSeq_genes_scored_compressed.hg{assembly_num}.tsv', sep='\t')
        # subsample dataframe
        subsample = df.sample(
            n=gene_ct-len(gene_list), 
            weights='score', 
            replace=False, 
            random_state=42
        )
        for row in subsample.itertuples():
            end = row.start + row.length
            sampled_genes.append({
                'gene':row.symbol,
                'start': row.start,
                'end': end,
                'chromosome': row.chrom
            })
        sampled_genes = sampled_genes + gene_list + sampled_chroms
        return sampled_genes
        

def create_sample_options(flattened_resources, sample_assembly, sample_cancer, location_options) -> List[Dict]:
    """
    Create sample options from the flattened resources (and maybe assembly
    and cancer ?)
    """
    
    sample_options = []
    # collect all unique samples
    unique_samples = set(x["sample"] for x in flattened_resources)

    # iterate thru unique samples
    for sample in unique_samples:
        sample_rows = [x for x in flattened_resources if x["sample"] == sample]
        
        # list files
        files = {}
        for row in sample_rows:
            file_name = row["file"]
            if file_name not in files:
                files[file_name] = {
                    "file": file_name,
                    "url": row["url"],
                    "fields": [],
                }
            # add data for file
            
            files[file_name]["fields"].append({
                "field": row["field"],
                "udi:data_type": row.get("udi:data_type", None),
                #"column_metadata": row.get("column_metadata", {}),
            })
        
        location_list=[]
        for loc in location_options:
            location_list.append(loc['gene'])
        
        # put together sample options
        sample_options.append({
            "sample": sample,
            "files": list(files.values()),
            "udi:assembly": sample_assembly,
            "udi:cancer-type": sample_cancer,
            "locations":location_list,
            "udi:cell-type":''
        })

    return sample_options

def expand_template(row, sample_options, entity_options, field_options, location_options, max_per_template):
    extract = extract_tags(row["query_template"])
    
    tags = extract["tags"]
        
    samples = extract["samples"]
    entities = extract["entities"]
    locations = extract["location"]
    fields = extract["fields"]
    
    constraints = expand_constraints(row["constraints"], tags) # added to convert to a list    
    
    s = constraint_solver(samples, entities, fields, locations, constraints, sample_options, entity_options, field_options, location_options)

    #return expand_solutions(row, tags, s)
    
    results = expand_solutions(row, tags, s)
    
    
    # add a limit on generation based on type. 
    taxonomy_type = row['taxonomy_type']
    if taxonomy_type == "location comparison" or taxonomy_type == "entity comparison" or taxonomy_type =="sample comparison":
        if len(results) > max_per_template:
            results = random.sample(results, max_per_template)
    
    return results


def expand_solutions(row, tags, solutions):
    result = []
    for s in solutions:
        expanded_row = row.copy()
        expanded_row["query_base"] = resolve_query_template(
            row["query_template"], tags, s
        )
        expanded_row["spec"] = resolve_spec_template(row["spec_template"], tags, s)
        expanded_row["caption"] = resolve_caption(row["caption"], tags, s)
        expanded_row["solution"] = cleanup_solution(s)
        result.append(expanded_row)
    return result

def cleanup_solution(solution):
    cleaned = {}
    for k in solution:
        newK = k.replace('_', '.')
        cleaned[newK] = solution[k]
        if 'F' in newK and 'foreignKeys' in cleaned[newK]:
            cleaned[newK].pop('foreignKeys')
    return cleaned

def resolve_query_template(query_template, tags, solution):
    query_base = query_template
    for tag in tags:
        if tag["field"]:
            k = tag["sample"] + "_" + tag["entity"] + "_" + tag["field"] 
            resolved = solution[k]["field"]
        elif tag["location"]:
            k = tag["sample"] + "_" + tag["location"] 
            resolved = solution[k]["gene"] # integrate chromosome here too?
        elif tag["entity"]:
            k = tag["sample"] + "_" + tag["entity"]
            resolved = solution[k]["udi:use"]
        else:
            resolved = solution[tag["sample"]]["sample"] #redefine entity as sample
        query_base = query_base.replace(f"<{tag['original']}>", resolved, 1)
    return query_base  

def expand_field(field, tags):
    for tag in tags:
        if tag['field'] == field:
            return tag['sample'] + '_' + tag['entity'] + '_' + tag['field']
    
def resolve_caption(caption, tags, solution):
    pattern = r"<([^>]+)>"
    
    while True:
        match = re.search(pattern, caption)
        
        if match == None:
            break
        
        match = match.group(0)
        content = match.strip("<>")
        
        parts = content.split(".")
        
        if len(parts) == 1:
            content = parts[0]
            if content.startswith("S"):
                sample = content
                resolved = solution[sample]["sample"]
            elif content.startswith("E"):
                resolved = solution["S_" + parts[0]]["udi:use"]
            
            elif content.startswith('L'):
                resolved = solution["S_" + parts[0]]["gene"]
        
        elif len(parts) == 2:
            
            left, right = parts
            
            if left.startswith("S"):
                left = left
            elif left.startswith("E") or left.startswith('L'):
                left = "S_" + left
            else:
                left = expand_field(left, tags)
            
            
            if right == 'cancer-type':
                resolved = solution[left]['udi:cancer-type']
            elif right == 'cell-type':
                resolved = solution[left]['udi:cell-type']
            elif right == 'geneStart':
                resolved = str(solution[left]['start'])
            elif right == 'geneEnd':
                resolved = str(solution[left]['end'])
            elif right == 'geneChr':
                resolved = str(solution[left]['chromosome'])
            else:
                resolved = solution[left + "_" + right]["name"]
                
        elif len(parts) == 3:
            left, mid, right  = parts
            
            if mid.startswith("E"):
                left = left + "_" + mid
            elif mid.startswith("L"):
                left = left + "_" + mid
            
            if right == 'geneName':
                resolved = solution[left]['gene']
            elif right == 'geneStart':
                resolved = str(solution[left]['start'])
            elif right == 'geneEnd':
                resolved = str(solution[left]['end'])
            elif right == 'geneChr':
                resolved = str(solution[left]['chromosome'])
            elif right == 'index-file':
                resolved = str(solution[left]['index-file'])
            else:
                resolved = solution[left + "_" + right]["name"]
        
        caption = caption.replace(match, resolved, 1)
    return caption
         
    
def resolve_spec_template(spec_template, tags, solution):
    spec = spec_template
    pattern = r"<([^>]+)>"
    
    while True:
        match = re.search(pattern, spec)
        
        if match == None:
            break
        match = match.group(0)
        content = match.strip("<>")
        
        parts = content.split(".")

        if len(parts) == 1:
            content = parts[0]
            if content.startswith("S"):
                sample = content
                resolved = solution[sample]["sample"]
            elif content.startswith("E"):
                resolved = solution["S_" + parts[0]]["udi:use"]
            
            elif content.startswith('L'):
                resolved = solution["S_" + parts[0]]["gene"]
            else:
                resolved = solution[expand_field(content, tags)]["sample"]
                
        elif len(parts) == 2:
            
            left, right = parts
            
            if left.startswith("S"):
                left = left
            elif left.startswith("E") or left.startswith('L'):
                left = "S_" + left
            else:
                left = expand_field(left, tags)
            
            if right == 'url':
                resolved = solution[left]['url']
            elif right == 'cancer-type':
                resolved = solution[left]['udi:cancer-type']
            elif right == 'cell-type':
                resolved = solution[left]['udi:cell-type']
            elif right == 'sample_name':
                resolved = solution[left]['sample']
            elif right == "field":
                resolved = solution[left]["field"]
            elif right == 'format':
                resolved = solution[left]["format"]
            #elif right == 'name':
            #    resolved = solution[left]["name"]
            elif right == 'assembly':
                resolved = solution[left]['udi:assembly']
                resolved = 'HG' + resolved[-2:]
            elif right == 'chr1':
                resolved = solution[left]['position-fields'][0]['chromosome-field']
            elif right == 'chr2':
                resolved = solution[left]['position-fields'][1]['chromosome-field']
            elif right == 'start1':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][0]
            elif right == 'end1':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][1]
            elif right == 'start2':
                resolved = solution[left]['position-fields'][1]['genomic-fields'][0]
            elif right == 'end2':
                resolved = solution[left]['position-fields'][1]['genomic-fields'][1]
            elif right == 'start':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][0]
            elif right == 'end':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][1]
            elif right == 'geneStart':
                resolved = str(solution[left]['start'])
            elif right == 'geneEnd':
                resolved = str(solution[left]['end'])
            elif right == 'geneChr':
                resolved = str(solution[left]['chromosome'])
            elif right == 'index-file':
                resolved = str(solution[left]['index-file'])
            else:
                resolved = solution[left + "_" + right]["name"]
                
        elif len(parts) == 3:
            left, mid, right  = parts
            
            #if left.startswith("S"):
            #    left = content
            #elif left.startswith("E") or content.startswith('L'):
            #    left = "S_" + left
            #else:
            #    left = expand_field(left, tags)
            
            
            if mid.startswith("E"):
                left = left + "_" + mid
            elif mid.startswith("L"):
                left = left + "_" + mid
               
            
            if right == 'url':
                resolved = solution[left]['url']
            elif right == 'sample_name':
                resolved = solution[left]['sample']
            elif right == 'geneName':
                resolved = solution[left]['gene']
            elif right == "field":
                resolved = solution[left]["field"]
            elif right == 'format':
                resolved = solution[left]["format"]
            elif right == 'chr1':
                resolved = solution[left]['position-fields'][0]['chromosome-field']
            elif right == 'chr2':
                resolved = solution[left]['position-fields'][1]['chromosome-field']
            elif right == 'start1':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][0]
            elif right == 'end1':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][1]
            elif right == 'start2':
                resolved = solution[left]['position-fields'][1]['genomic-fields'][0]
            elif right == 'end2':
                resolved = solution[left]['position-fields'][1]['genomic-fields'][1]
            elif right == 'start':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][0]
            elif right == 'end':
                resolved = solution[left]['position-fields'][0]['genomic-fields'][1]
            elif right == 'geneStart':
                resolved = str(solution[left]['start'])
            elif right == 'geneEnd':
                resolved = str(solution[left]['end'])
            elif right == 'geneChr':
                resolved = str(solution[left]['chromosome'])
            elif right == 'index-file':
                resolved = str(solution[left]['index-file'])
            else:
                resolved = solution[left + "_" + right]["name"]
                
                
        elif len(parts) == 5:
            S1, r, S2, id, source = parts
            if S1[0] != "S" or S2[0] != "S" or r != "r" or id != "id" or source not in ["from", "to"]:
                raise ValueError(
                    f"Invalid match: {match}. Unexpected formatting of spec template tag."
                )
            S2_name = solution[S2]["source"]
            # resolved = solution[E1]["foreignKeys"][E2_name]["id"][source]
            # What needs to happen here, is it should loop over foreign keys to find if reference.resource matches E2_name
            # and then if source is 'from' return fields else return reference.fields
            foreignKeys = solution[S1]["foreignKeys"]
            matchedKey = next(
                (fk for fk in foreignKeys if fk["reference"]["resource"] == S2_name),
                None,
            )
            if matchedKey is None:
                raise ValueError(
                    f"Invalid match: {match}. Could not find foreign key for {S1} to {S2}"
                )
            if source == "from":
                resolved = matchedKey["fields"]
            else:
                resolved = matchedKey["reference"]["fields"]
            if len(resolved) == 1:
                resolved = resolved[0]
            else:
                resolved = f"[\"{'","'.join(resolved)}\"]"
                match = f"\"{match}\"" # add quotes because the replace needs to replace the string with a list of strings.
        else:
            raise ValueError(
                f"Invalid match: {match}. Unexpected formatting length of spec template tag."
            )
        
        spec = spec.replace(match, resolved, 1)

    
    # Special care needs to take place to handle comparisons
    # e.g. {lte} should be replaced with <=
    # this must happen after the other replacements that are 
    # looking for < and > characters.
    comparisons = [
        {"content": "{lte}", "resolved": "<="},
        {"content": "{gte}", "resolved": ">="},
        {"content": "{lt}", "resolved": "<"},
        {"content": "{gt}", "resolved": ">"}
    ]
    for comparison in comparisons:
        spec = spec.replace(comparison["content"], comparison["resolved"])
    
    return spec


def extract_tags(text: str) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Example input:
     "This is just to test <E> and <E1> and <E2> and <F:o> and <E.F:o> and <E1.F1:N> and <E2.F2:o|n> and more text"
    Example output:
        [
            {"original": "E", "entity": "E", "field": None, "field_type": None},
            {"original": "E1", "entity": "E1", "field": None, "field_type": None},
            {"original": "E2", "entity": "E2", "field": None, "field_type": None},
            {"original": "F:o", "entity": None, "field": "F", "field_type": ["o"]},
            {"original": "E1.F1:n", "entity": "E1", "field": "F1", "field_type": ["n"]},
            {"original": "E2.F2:o|n", "entity": "E2", "field": "F2", "field_type": ["o", "n"]}
        ]
        
    """
    pattern = r"<([^>]+)>"
    matches = re.findall(pattern, text)

    tags = []
    # match: each time the pattern appears in the text
    # <F.p.q> or <F.p>
    # <F.g>
    for match in matches:
        parts = match.split(".")
        
        sample, entity, field, location, field_type = None, None, None, None, None
        if len(parts) == 1:
            first = parts[0]
            # check if sample, field, entity, or location
            if first.startswith("S"):
                sample = first
            elif first.startswith("L"):
                location = first
            elif first.startswith("E"):
                entity=first
            else:
                field=first
                
        elif len(parts) == 2:
            first, second = parts
            sample=first
            if second.startswith("L"):
                location = second
            elif second.startswith("E"):
                entity = second
            elif second.startswith('c'):
                field=None
            else:
                field=second
        elif len(parts) == 3:
            first, second, third=parts
            sample=first
            if second.startswith("L"):
                location = second
            
            elif second.startswith("E"):
                entity = second
                
            #if parts[2] == "geneName":
            #    sample=first
            #    entity=second
            #    field=None
            else:
                sample=first
                entity=second
                field=third
                
        else:
            raise ValueError(
                f"Invalid match: {match}. There should only be 1 or 2 '.'"
            )

        if field:
            field_parts = field.split(":")

            if len(field_parts) == 2:
                field, field_type = field_parts          
                
                #if len(field_type)==1:
                field_type = [
                    {"n": "nominal", 
                    "o": "ordinal", 
                    "q": "quantitative", 
                    "g": "genomic",
                    "g&q": "quantitative genomic",
                    "g&c": "categorical genomic",
                    "p": "point",
                    "p&n": "nominal point",
                    "p&o":"ordinal point",
                    "p&q":'quantitative point',
                    "s": "segment",
                    "s&n": "nominal segment",
                    "s&o":"ordinal segment",
                    "s&q": "quantitative segment",
                    "c": "connective"}[t]
                    for t in field_type.split("|")
                ]
                
                #else:
                #    raise ValueError(
                #        f"Invalid match: {match}. Field type must be specified"
                #    )
        tags.append(
            {
                "sample": sample,
                "entity": entity,
                "field": field,
                "location": location,
                "allowed_fields": field_type,
                "original": match,
            }
        )
     
    # infer sample and entity  
    infer_entity(tags) 
    infer_sample(tags)
    
    samples = set([tag["sample"] for tag in tags])
    #fields = set([tag["field"] for tag in tags if tag["field"]])
    entities = set(
        [str(tag["sample"]) + "_" + tag["entity"] for tag in tags if tag["entity"]]
    )
    fields = set(
        [str(tag["sample"]) + "_" + tag["entity"] + "_" + tag["field"] for tag in tags if tag["field"]]
    )
    
    locations = set(
        [str(tag["sample"]) + "_" + tag["location"] for tag in tags if tag["location"]]
    )
    
    return {"tags": tags, "samples": list(samples), "entities": list(entities), "location": list(locations), "fields": list(fields)}


def infer_sample(
    tags: List[Dict[str, Union[str, List[str]]]],
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Infer the sample based on the other samples. If none is provided, default to S.
    If there is an empty sample and multiple other samples defined, thwrow an error.
    """
    defined_samples = [tag["sample"] for tag in tags if tag["sample"]]
    
    unique_samples = set(defined_samples)

    if len(unique_samples) > 1 and any(not tag["sample"] for tag in tags):
        raise ValueError("Multiple samples defined, cannot infer empty sample.")
    for tag in [x for x in tags if not x["sample"]]:
        tag["sample"] = "S"
    return tags

def infer_entity(
    tags: List[Dict[str, Union[str, List[str]]]],
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Infer the entity based on the other entities. If none is provided, default to E.
    If there is an empty entity and multiple other entities defined, throw an error.
    """
    defined_entities = [tag["entity"] for tag in tags if tag["entity"]]
    unique_entities = set(defined_entities)
            
    #if len(unique_entities) > 1 and any(not tag["entity"] for tag in tags):
    #    raise ValueError("Multiple entities defined, cannot infer empty entity.")
    
    for tag in [x for x in tags if not x["entity"] and not x["original"][0] == 'S']:
    #for tag in [x for x in tags if not x["entity"] and x['sample'][0] != "S" ]:
        tag["entity"] = "E"
        
    return tags


def expand_constraints(
    constraints: List[str], tags: List[Dict[str, Union[str, List[str]]]]
) -> List[str]:  # type: ignore
    """
    the current constraints will be expanded a bit
        e.g. F.c > 4 → F["udi:cardinality"] > 4
    the tags will add constraints for each field type
    and will add a constraint to ensure unique fields
    """
    expanded_constraints = []
    #constraints.split(',')
    if isinstance(constraints, str):
        constraints = ast.literal_eval(constraints)
        
    for constraint in constraints:
        # E1.r.E2.c.to → E1.r.E2['cardinality'].to
        resolved = constraint.replace(".c", "['udi:cardinality']")
        
        resolved = constraint.replace(".a", "['udi:assembly']")
        
        # E1.r.E2['cardinality'].to → E1.r[E2['entity']]['cardinality'].to
        resolved, isErConstraint = resolve_related_entity(resolved)
       
        if isErConstraint:
            relationship_existance = create_relationship_existence_constraint(constraint)
            expanded_constraints.append(relationship_existance)
        # E1.r[E2["name"]]['cardinality'].to →
        # E1['relationships][E2["name"]]['cardinality'].to
        resolved = resolved.replace(".r", "['foreignKeys']")
        # E1['relationships][E2["name"]]['cardinality'].to →
        # E1['relationships][E2["name"]]['cardinality']['to']
        resolved = resolved.replace(".to", "['to']")
        resolved = resolved.replace(".from", "['from']")
        resolved = resolved.replace(".fields", "['fields']")
        resolved = resolved.replace(".name", "['name']")
        #  E1.F1 → E1_F1
        resolved = resolved.replace(".", "_")
        #  F → E_F1

        resolved = add_default_entity(resolved)
        expanded_constraints.append(resolved)
        
    
    expanded_constraints.extend(
        [
            f"{tag['sample']}_{tag['entity']}_{tag['field']}['udi:data_type'] in {tag['allowed_fields']}"
            for tag in tags
            if tag["field"]
        ]
    )
    
    # Ensure fields are not repeated
    unique_fields = set(
        [str(tag["sample"]) + "_" + tag["entity"] + "_" + tag["field"] for tag in tags if tag["field"]]
    )
    # if len(unique_fields) > 1:
    #     for field in unique_fields:
    #         other_fields = unique_fields - {field}
    #         expanded_constraints.append(f"{field} not in {other_fields}")

    if len(unique_fields) > 1:
        for field in unique_fields:
            other_fields = unique_fields - {field}
            name_str = "['field']"
            # other_fields_string = (
            #     "[" + ",".join([str(x) + name_str for x in other_fields]) + "]"
            # )
            
            # expanded_constraints.append(
            #   f"{field + name_str} not in {other_fields_string}"
            # )

    # ensure that samples are not repeated
    unique_samples = set([tag["sample"] for tag in tags])
    if len(unique_samples) > 1:
        for sample in unique_samples:
            other_samples = unique_samples - {sample}
            e_str = "['sample']"
            other_samples_string = (
                "[" + ",".join([str(x) + e_str for x in other_samples]) + "]"
            )
            expanded_constraints.append(
              f"{sample + e_str} not in {other_samples_string}"
            )
            expanded_constraints.append(
               f"{sample + e_str} not in {other_samples_string}"
            )

    # ensure that fields belong to their entity and sample
    for field in unique_fields:
        sample = field.split("_")[0]
        #expanded_constraints.append(f"{field}['sample'] == {sample}['sample']")
        entity = field.split("_")[1]
        #expanded_constraints.append(f"{field}['sample'] == {sample + "_" + entity}['sample']")
        #expanded_constraints.append(f"{field}['file'] == {sample + "_" + entity}['name']")

    return expanded_constraints


def create_relationship_existence_constraint(constraint: str) -> str:
    '''
    given an input E1.r.E2.c.to == 'one'
    want to generate a relationship existence constraint:
        E2['entity'] in [fk['reference']['resource'] for fk in E1['foreignKeys']]
    '''
    parts = constraint.split('.')
    if len(parts) < 3:
        raise ValueError("Unexpected relationship constraint length:", constraint)
    S1, r, S2 = parts[:3]
    if (S1[0] != 'S') or (S2[0] != 'S') or (r != 'r'):
        raise ValueError("Unexpected relationship constraint:", constraint)
    existence_constraint =  f"{S2}['sample'] in [fk['reference']['resource'] for fk in {S1}['foreignKeys']]"
    return existence_constraint

def resolve_related_entity(text): 
    # use regex to replace E1.r.E2.c.to with:
    # {fk['reference']['resource']:fk for fk in E1['foreignKeys']}.r[E2['entity']].c.to
    # other things (.c, .to) well be resolved elsewhere
    # assumes that the only time .E exists is when finding a relationship
    foundConstraint = False
    pattern = r'\.S[0-9]*'
    while re.search(pattern, text):
        foundConstraint = True
        match = re.search(pattern, text).group(0)
        resolved = f"[{match.lstrip('.')}['sample']]"
        #(f'Text before: {text}')
        text = text.replace(match, resolved)
        
    if foundConstraint:
        pattern = r'S[0-9]*\.r'
        while re.search(pattern, text):
            match = re.search(pattern, text).group(0)
            S_number = match.split(".")[0].lstrip("S")
            resolved = "{fk['reference']['resource']:fk for fk in S" + str(S_number) + "['foreignKeys']}"
            text = text.replace(match, resolved)
            
    return text, foundConstraint

def add_default_entity(text):
    # Use regex to match "F" that is not preceded by "_" and replace it with "S_E_F"    
    modified_text = re.sub(r'(?<!_)F', r'S_E_F', text)
    # replace L that does not have _ to replace with S_L
    modified_text = re.sub(r'(?<!_)E', r'S_E', modified_text)
    # replace L that does not have _ to replace with S_L
    modified_text = re.sub(r'(?<!_)L', r'S_L', modified_text)
    return modified_text

def constraint_solver(
    samples: List[str],
    entities: List[str],
    fields: List[str],
    locations: List[str],
    constraints: List[str],
    sample_options: List[Dict[str, Union[str, int]]],
    entity_options: List[Dict[str, Union[str, int]]],
    field_options: List[Dict[str, Union[str, int]]],
    location_options:  List[Dict[str, Union[str, int]]]
) -> List[Dict[str, str]]:
    problem = Problem()
    
    
    
    problem.addVariables(fields, field_options)
    problem.addVariables(samples, sample_options)
    problem.addVariables(entities, entity_options)
    problem.addVariables(locations, location_options)
            
    for constraint in constraints:
        problem.addConstraint(constraint) 
    
    s = problem.getSolutions()
        
    return s

if __name__ == "__main__":
    
    with open('all-schema.json', 'r') as f:
        schema=json.load(f)
    df=pd.read_csv('spec_generation_test.tsv', sep='\t')

    expanded_df = expand(df, schema)
    print(expanded_df)

    expanded_df.to_csv("spec_generation_output.csv")