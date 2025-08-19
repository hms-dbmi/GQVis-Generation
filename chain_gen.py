import random
import json

import pprint

def create_chains(followups, length_dist=[0, 0, 40, 30, 30, 25, 15]):
    # 1: iterate through starts.
    start_queries = followups.keys()
    all_chains = [] 
    for query in start_queries:
        for i in range(len(length_dist)):
            all_chains += generate_chains(query, followups, i, length_dist[i])
    
    return all_chains
        
def generate_chains(start_query, followups, length, qty):
    chains = []
    if length > 1:
        print('here')
        print(qty)
        while qty > 1:
            # 1: select length - 1 followups from followups at random
            query_options = list(followups[start_query])
            next_queries = random.choices(query_options, k = length - 1)
            
            chains += [write_json(start_query, next_queries)]
            
            qty -= 1
    
    return chains
        

def write_json(start_query, next_queries):
    jsons = []
    for i in range(len(next_queries)):
        if i == 0:
            jsons.append(
                {
                "template": {
                    "start": start_query,
                    "end": next_queries[i][0]
                },
                "transition_type": next_queries[i][1],
                "subtype": next_queries[i][2],
                "chain_step":i
                })
            print(jsons)
        else:
            jsons.append(
                {
                "template": {
                    "start": next_queries[i-1][0],
                    "end": next_queries[i][0]
                },
                "transition_type": next_queries[i][1],
                "subtype": next_queries[i][2],
                "chain":i
                }
            )
    print("The jsons")
    return jsons
    

def main():
    followups=dict()

    followups['What is the <E> data?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Add an ideogram of <S>.', 'comparative change', 'ideogram'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a detail view of <E> at <L>.', 'visual', 'detail view'),
        ('Stratify the <E> data.', 'data stratification', ''),
    }

    followups['What is the <E> data at <L>?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Add an ideogram of <S> at <L>.', 'comparative change', 'ideogram'),
        ('Overlay <E0> at <L>.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a whole-genome view of <E>.', 'visual', 'general view'),
        ('Stratify the <E> data.', 'data stratification', ''),
        ('Add an ideogram of <S>.', 'comparative change', 'ideogram')
        
    }

    followups['How does the <E> compare at <L1> and <L2>?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Add an ideogram of <S> at <L>.', 'comparative change', 'ideogram'),
        ('Overlay <E0> at <L1> and <L2>.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a whole-genome view of <E>.', 'visual', 'general view'),
        ('Stratify the <E> data.', 'data stratification', ''),
    }
    followups['How does the <S1.E> in <S1> compare to the <S2.E> in <S2>?']={
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition')
    }

    followups['What is the distribution of <E>?']={
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a detail view of <E> at <L>.', 'visual', 'detail view'),
        ('Stratify the <E> data.', 'data stratification', '')
    }
    followups['How does <E> vary across the genome?']={
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a detail view of <E> at <L>.', 'visual', 'detail view'),
        ('Stratify the <E> data.', 'data stratification', ''),
    }

    followups['What is the <E> data as an area chart?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Overlay <E> as a line chart.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a detail view of <E> at <L>.', 'visual', 'detail view')
    }

    followups['What is the <E> data as an line chart?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0>.', 'comparative change', 'addition'),
        ('Add a view of <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <S0.E> in <S0> at <L>.', 'comparative change', 'addition'),
        ('Compare with <E> at <L0>.', 'comparative change', 'addition'),
        ('Add a view of <E> at <L0>.', 'comparative change', 'addition'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Overlay <E> as a line chart.', 'overlay', ''),
        ('Make <E> circular.', 'visual', 'circular'),
        ('Give <E> a linear layout.', 'visual ', 'linear'),
        ('Add a detail view of <E> at <L>.', 'visual', 'detail view')
    }
    
    followups['How does <E1> compare with <E2>?'] = {
        ('Add an <E0> data view.', 'comparative change', 'addition'),
        ('Compare with <E0>.', 'comparative change', 'addition'),
        ('Overlay <E0>.', 'overlay', ''),
        ('Overlay <E1> and <E2>', 'overlay', '')
    }
    
    followups['How does <E1> compare with <E2> at <L>?'] = {
        ('Add the <E0> data at <L>.', 'comparative change', 'addition'),
        ('Compare with <E0> at <L>.', 'comparative change', 'addition'),
        ('Overlay <E1> and <E2> at <L>', 'overlay', '')
    }
    

    with open("chains.json", "w") as json_file:
        
        chains = create_chains(followups)
        print(f'{len(chains)} chains produced')
            
        json.dump(chains, json_file, indent=4)
    

main()
