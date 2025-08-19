import pandas as pd
#from udi_grammar_py import Chart, Op, rolling
from enum import Enum
import json
#import gosling as gos

class QueryType(Enum):
    QUESTION = "question"
    UTTERANCE = "utterance"

class ChartType(Enum):
    #SCATTERPLOT = "scatterplot"
    BARCHART = "barchart"
    POINT = 'point'
    LINE = 'line',
    CONNECTIVITY = 'connectivity',
    COMPARATIVE_STACK = 'comparative_stack',
    RECTANGLE = 'rectangle'
    #GROUPED_BAR = "stacked_bar"
    #STACKED_BAR = "stacked_bar"
    #NORMALIZED_BAR = "stacked_bar"
    #CIRCULAR = "circular"
    #TABLE = "table"
    #LINE = "line"
    #AREA = "area"
    #GROUPED_LINE = "grouped_line"
    #GROUPED_AREA = "grouped_area"
    #GROUPED_SCATTER = "grouped_scatter"
    #HEATMAP = "heatmap"
    #HISTOGRAM = "histogram"
    #DOT = "dot"
    #GROUPED_DOT = "grouped_dot"


def add_row(df, query_template, spec, constraints, justification, query_type: QueryType, chart_type: ChartType):
    spec_key_count = get_total_key_count(spec)
    if spec_key_count <= 12:
        complexity = "simple"
    elif spec_key_count <= 24:
        complexity = "medium"
    elif spec_key_count <= 36:
        complexity = "complex"
    else:
        complexity = "extra complex"
    df.loc[len(df)] = {
        "query_template": query_template,
        "constraints": constraints,
        "spec_template": json.dumps(spec),
        "query_type": query_type.value,
        "creation_method": "template",
        "chart_type": chart_type.value,
        "chart_complexity": complexity,
        "spec_key_count": spec_key_count,
        "justification": justification
    }
    return df

def get_total_key_count(nested_dict):
    if isinstance(nested_dict, dict):
        return sum(get_total_key_count(value) for value in nested_dict.values())
    elif isinstance(nested_dict, list):
        return sum(get_total_key_count(item) for item in nested_dict)
    else:
        return 1

    
def generate():
    df = pd.DataFrame(
        columns=[
            "query_template",
            "constraints",
            "spec_template",
            "query_type",
            "creation_method",
            "chart_type",
            "chart_complexity",
            "spec_key_count",
            "justification"
        ]
    )
    
    

    # ----------- Define recurring constraints ---------------------------------
    overlap = "F1['name'] in F2['udi:overlapping_fields'] or F2['udi:overlapping_fields'] == 'all'"
    same_assembly = "S1['udi:assembly'] == S2['udi:assembly']"
    
    different_genes="L1['gene'] != L2['gene']"
    different_samples="S1['sample'] != S2['sample']"
    different_entities ="S2.E['url'] != S1.E['url']"

    same_location = "S1.L['gene'] in S2['locations']"
    sample_contains_entity="S1.E['name'] == S2.E['name']"
    
    entity_in_sample = "S['sample'] == E0['sample']"

    # ----------- Define recurring justifications ------------------------------
    new_entity = "An additional view was added to reflect the new entity requested by the user."
    new_entity_at_loc = "An additional view at the given location was added to reflect the new entity requested by the user."
    new_location = "An additional view was added to reflect the new location requested by the user."
    new_sample = "An additional sample was added to reflect the new location requested by the user."
    
    new_heatmap="The data is displayed in a heatmap because it highlights the physical contacts between pairs of genomic regions."
    new_chipseq_bar="The added ChIP-seq data is shown as a bar graph to represent protein interactions, with bar height corresponding to the frequency of interaction at a given location."
    new_rna_bar="The added RNA-seq data is shown as a bar graph to represent gene expression levels, with bar height corresponding to the transcript abundance at a given location."
    new_atac_bar="The added ATAC-seq data is shown as a bar graph to represent chromatin accessibility, with bar height corresponding to the openness at a given location."
    new_sv = "Structural variant (SV) data was added as a connectivity plot. The connectivity plot enables viewing of the SV breakpoints between and within chromosomes."
    new_cna = "CNA data was added as a series of bars, with the rectangle heights displaying frequency of the alteration."
    new_point ="Point mutation data was added at the user request. This is displayed in a point plot, with each point representing the genomic location of a point mutation."
    
    ideogram = "The ideogram allows the user to visualize the region of interest across the full genome view."
    ideogram_at_location = "The ideogram is centered at the user-specified location to display the region in context."
    # ------------------------------------------------------------------------------------------
    # IDEOGRAM  --------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an ideogram of <S>.",
        spec=(
            {
            "title": "Ideogram",
            "alignment": "overlay",
            "data": {
              "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.<S.assembly>.Human.CytoBandIdeogram.csv",
              "type": "csv",
              "chromosomeField": "Chromosome",
              "genomicFields": [
                "chromStart",
                "chromEnd"
              ]
            },
            "tracks": [
              {
                "mark": "rect",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ],
                    "not": True
                  }
                ]
              },
              {
                "mark": "triangleRight",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ]
                  },
                  {
                    "type": "filter",
                    "field": "Name",
                    "include": "q"
                  }
                ]
              },
              {
                "mark": "triangleLeft",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ]
                  },
                  {
                    "type": "filter",
                    "field": "Name",
                    "include": "p"
                  }
                ]
              }
            ],
            "color": {
              "field": "Stain",
              "type": "nominal",
              "domain": [
                "gneg",
                "gpos25",
                "gpos50",
                "gpos75",
                "gpos100",
                "gvar",
                "acen"
              ],
              "range": [
                "white",
                "lightgray",
                "gray",
                "gray",
                "black",
                "#7B9CC8",
                "#DC4542"
              ]
            },
            "size": {
              "value": 18
            },
            "x": {
              "field": "chromStart",
              "type": "genomic",
              
            },
            "xe": {
              "field": "chromEnd",
              "type": "genomic"
            },
            "strokeWidth": {
              "value": 0
            }
          }
        ),
        constraints=[
        ],
        justification=[
            ideogram
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add an ideogram of <S> at <L>",
        spec=(
            {
            "title": "  Ideogram",
            "alignment": "overlay",
            "data": {
              "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.<S.assembly>.Human.CytoBandIdeogram.csv",
              "type": "csv",
              "chromosomeField": "Chromosome",
              "genomicFields": [
                "chromStart",
                "chromEnd"
              ]
            },
            "tracks": [
              {
                "mark": "rect",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ],
                    "not": True
                  }
                ]
              },
              {
                "mark": "triangleRight",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ]
                  },
                  {
                    "type": "filter",
                    "field": "Name",
                    "include": "q"
                  }
                ]
              },
              {
                "mark": "triangleLeft",
                "dataTransform": [
                  {
                    "type": "filter",
                    "field": "Stain",
                    "oneOf": [
                      "acen"
                    ]
                  },
                  {
                    "type": "filter",
                    "field": "Name",
                    "include": "p"
                  }
                ]
              }
            ],
            "color": {
              "field": "Stain",
              "type": "nominal",
              "domain": [
                "gneg",
                "gpos25",
                "gpos50",
                "gpos75",
                "gpos100",
                "gvar",
                "acen"
              ],
              "range": [
                "white",
                "lightgray",
                "gray",
                "gray",
                "black",
                "#7B9CC8",
                "#DC4542"
              ]
            },
            "size": {
              "value": 18
            },
            "x": {
              "field": "chromStart",
              "type": "genomic",
              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}
            },
            "xe": {
              "field": "chromEnd",
              "type": "genomic"
            },
            "strokeWidth": {
              "value": 0
            },
            "width": 600,
            "height": 50
          }
        ),
        constraints=[
        ],
        justification=[
            ideogram_at_location
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.BARCHART
    )
    
    
    # --------------------------------------------------------------------
    # ------------- comparative additions --------------------------------
    # --------------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an <E0> data view",
        spec=(
            {
            "title": "Contacts across whole genome",
            "tracks": [{
                    "data": {
                        "url": "<E0.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top"},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Compare with <E0>",
        spec=(
            {
            "title": "Contacts across whole genome",
            "tracks": [{
                    "data": {
                        "url": "<E0.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top"},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            new_entity, 
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            {
            "title": "Contacts across <L>",
            "tracks": [{
                    "data": {
                        "url": "<E0.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            {
            "title": "Contacts across <L>",
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
            [{
                "title":"Contacts at <S0>",
                "data": {
                    "url": "<S0.E.url>",
                    "type": "matrix"
                },
                "mark": "bar",
                "x": {"field": "xs", "type": "genomic", "axis": "top"},
                "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                "y": {"field": "ys", "type": "genomic", "axis": "left"},
                "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                "color": {"field": "value", "type": "quantitative", "range": "warm"},
                "width": 600,
                "height": 600  
            }]
        ),
        constraints=[
            "S0.E['udi:use'] == 'contact'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
            [{
                "title":"Contacts at <S0>",
                "data": {
                    "url": "<S0.E.url>",
                    "type": "matrix"
                },
                "mark": "bar",
                "x": {"field": "xs", "type": "genomic", "axis": "top"},
                "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                "y": {"field": "ys", "type": "genomic", "axis": "left"},
                "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                "color": {"field": "value", "type": "quantitative", "range": "warm"},
                "width": 600,
                "height": 600  
            }]
        ),
        constraints=[
            "S0.E['udi:use'] == 'contact'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
            [{
                "title":"Contacts in <S0> at <L>",
                "data": {
                    "url": "<S0.E.url>",
                    "type": "matrix"
                },
                "mark": "bar",
                "x": {"field": "xs", "type": "genomic", "axis": "top",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                "y": {"field": "ys", "type": "genomic", "axis": "left"},
                "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                "color": {"field": "value", "type": "quantitative", "range": "warm"},
                "width": 600,
                "height": 600  
            }]
        ),
        constraints=[
            "S0.E['udi:use'] == 'contact'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            [{
                "title":"Contacts at <S0> in <L>",
                "data": {
                    "url": "<S0.E.url>",
                    "type": "matrix"
                },
                "mark": "bar",
                "x": {"field": "xs", "type": "genomic", "axis": "top",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                "y": {"field": "ys", "type": "genomic", "axis": "left"},
                "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                "color": {"field": "value", "type": "quantitative", "range": "warm"},
                "width": 600,
                "height": 600  
            }]
        ),
        constraints=[
            "S0.E['udi:use'] == 'contact'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
            "title": "Contacts across <L0>",
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            new_location,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
            "title": "Contacts across <L0>",
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            new_location,
            new_heatmap
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    # chipseq views ------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an <E0> data view",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            new_entity, 
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            },
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'peaks' or S0.E['udi:use'] == 'conservative peaks'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'peaks' or S0.E['udi:use'] == 'conservative peaks'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'peaks' or S0.E['udi:use'] == 'conservative peaks'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'peaks' or S0.E['udi:use'] == 'conservative peaks'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "E['sample'] == S.E['sample']"
        ],
        justification=[
            new_location,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            new_location,
            new_chipseq_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    


    # RNA views ------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an <E0> data view",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            new_entity, 
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            },
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'gene expression' or S0.E['udi:use'] == 'gene expression'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'gene expression' or S0.E['udi:use'] == 'gene expression'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'gene expression' or S0.E['udi:use'] == 'gene expression'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'gene expression' or S0.E['udi:use'] == 'gene expression'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            new_location,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            new_location,
            new_rna_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )




    # atac views ------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an <E0> data view",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample      
        ],
        justification=[
            new_entity,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample        
        ],
        justification=[
            new_entity, 
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample        
        ],
        justification=[
            new_entity_at_loc,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            {
            "title": "<E0>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample        
        ],
        justification=[
            new_entity_at_loc,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            },
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'atac peaks' or S0.E['udi:use'] == 'conservative atac peaks'",
            "S0.E['sample'] == S0['sample']"        
        ],
        justification=[
            new_sample,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'atac peaks' or S0.E['udi:use'] == 'conservative atac peaks'",
            "S0.E['sample'] == S0['sample']"        
        ],
        justification=[
            new_sample,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
            
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'atac peaks' or S0.E['udi:use'] == 'conservative atac peaks'",
            "S0.E['sample'] == S0['sample']"        
        ],
        justification=[
            new_sample,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            {
                "tracks":
                    [
                        {
                        "title":"<S0.E> for <S0>",
                        "data": {
                            "url": "<S0.E.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },

                        "mark": "bar",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom",
                              "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                        
                    ]
            }
        ),
        constraints=[
            "S0.E['format'] == 'bigbed' or S0.E['format'] == 'bigwig'",
            "S0.E['udi:use'] == 'atac peaks' or S0.E['udi:use'] == 'conservative atac peaks'",
            "S0.E['sample'] == S0['sample']"        
        ],
        justification=[
            new_sample,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == S['sample']"        
        ],
        justification=[
            new_location,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
            "title": "<E>",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == S['sample']"        
        ],
        justification=[
            new_location,
            new_atac_bar
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )


    # -------------------------------------------------------------------
    # CHROMOSCOPE DATA FOLLOW UPS
    # -------------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="Add an <E0> data view.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic"},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic"},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic",
                          "domain":{"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic",
                          "domain":{"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
            {
                "title": "Structural variants in <S0>",
                "tracks": [
                    {
                    "data": {
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<S0.E.chr1>", "genomicFields":["<S0.E.start1>", "<S0.E.end1>"]},
                            {"chromosomeField": "<S0.E.chr2>", "genomicFields":["<S0.E.start2>", "<S0.E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<S0.E.start1>", "type": "genomic"},
                    "xe": {"field": "<S0.E.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'sv'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            {
                "title": "Structural variants in <S0>",
                "tracks": [
                    {
                    "data": {
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<S0.E.chr1>", "genomicFields":["<S0.E.start1>", "<S0.E.end1>"]},
                            {"chromosomeField": "<S0.E.chr2>", "genomicFields":["<S0.E.start2>", "<S0.E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<S0.E.start1>", "type": "genomic"},
                    "xe": {"field": "<S0.E.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'sv'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
            {
                "title": "Structural variants in <S0>",
                "tracks": [
                    {
                    "data": {
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<S0.E.chr1>", "genomicFields":["<S0.E.start1>", "<S0.E.end1>"]},
                            {"chromosomeField": "<S0.E.chr2>", "genomicFields":["<S0.E.start2>", "<S0.E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<S0.E.start1>", "type": "genomic",
                          "domain":{"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "<S0.E.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'sv'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
            {
                "title": "Structural variants in <S0>",
                "tracks": [
                    {
                    "data": {
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<S0.E.chr1>", "genomicFields":["<S0.E.start1>", "<S0.E.end1>"]},
                            {"chromosomeField": "<S0.E.chr2>", "genomicFields":["<S0.E.start2>", "<S0.E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<S0.E.start1>", "type": "genomic",
                          "domain":{"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "<S0.E.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'sv'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
                "title": "Structural variants at <L0>",
                "tracks": [
                    {
                    "data": {
                        "url": "<E.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                            {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E.start1>", "type": "genomic",
                          "domain":{"chromosome": "<L0.geneChr>", "interval": ["<L0.geneStart>", "<L0.geneEnd>"]}},
                    "xe": {"field": "<E.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            new_location,
            new_sv
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    # copy number data
    
    df = add_row(
        df,
        query_template="Add an <E0> data view.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E0.url>",
                        "type": "csv",
                        "chromosomeField": "<E0.chr1>",
                        "genomicFields": ["<E0.start>", "<E0.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E0.start>",
                        "type": "genomic"
                    },
                    "xe": {
                        "field": "<E0.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E0.url>",
                        "type": "csv",
                        "chromosomeField": "<E0.chr1>",
                        "genomicFields": ["<E0.start>", "<E0.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E0.start>",
                        "type": "genomic"
                    },
                    "xe": {
                        "field": "<E0.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E0.url>",
                        "type": "csv",
                        "chromosomeField": "<E0.chr1>",
                        "genomicFields": ["<E0.start>", "<E0.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E0.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<E0.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E0.url>",
                        "type": "csv",
                        "chromosomeField": "<E0.chr1>",
                        "genomicFields": ["<E0.start>", "<E0.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E0.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<E0.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
                {
                "tracks":[{
                    "title": "Copy Number Variants in <S0>",
                    "data": {
                        "separator": "\t",
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "chromosomeField": "<S0.E.chr1>",
                        "genomicFields": ["<S0.E.start>", "<S0.E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<S0.E.start>",
                        "type": "genomic",
                    },
                    "xe": {
                        "field": "<S0.E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'cna'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
                {
                "tracks":[{
                    "title": "Copy Number Variants in <S0>",
                    "data": {
                        "separator": "\t",
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "chromosomeField": "<S0.E.chr1>",
                        "genomicFields": ["<S0.E.start>", "<S0.E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<S0.E.start>",
                        "type": "genomic",
                    },
                    "xe": {
                        "field": "<S0.E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'cna'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
                {
                "tracks":[{
                    "title": "Copy Number Variants in <S0> at <L>",
                    "data": {
                        "separator": "\t",
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "chromosomeField": "<S0.E.chr1>",
                        "genomicFields": ["<S0.E.start>", "<S0.E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<S0.E.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<S0.E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'cna'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
                {
                "tracks":[{
                    "title": "Copy Number Variants in <S0> at <L>",
                    "data": {
                        "separator": "\t",
                        "url": "<S0.E.url>",
                        "type": "csv",
                        "chromosomeField": "<S0.E.chr1>",
                        "genomicFields": ["<S0.E.start>", "<S0.E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<S0.E.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<S0.E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "S0.E['udi:use'] == 'cna'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E.url>",
                        "type": "csv",
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start>", "<E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L0.geneChr>",
                        "interval":["<L0.geneStart>", "<L0.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            new_location,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E.url>",
                        "type": "csv",
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start>", "<E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E.start>",
                        "type": "genomic",
                        "domain": {
                        "chromosome": "<L0.geneChr>",
                        "interval":["<L0.geneStart>", "<L0.geneEnd>"]
                        }
                    },
                    "xe": {
                        "field": "<E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            new_location,
            new_cna
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    
    # point mutation data
    
    df = add_row(
        df,
        query_template="Add an <E0> data view.",
        spec=(
            
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E0.url>",
                    "indexUrl": "<E0.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic"
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0>.",
        spec=(
            
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E0.url>",
                    "indexUrl": "<E0.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic"
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            new_entity,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add the <E0> data at <L>.",
        spec=(
            
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E0.url>",
                    "indexUrl": "<E0.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
            
        ),
        constraints=[
            "E0['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <E0> at <L>.",
        spec=(
            
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E0.url>",
                    "indexUrl": "<E0.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
            
            
            
        ),
        constraints=[
            "E0['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            new_entity_at_loc,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0>.",
        spec=(
                {
            "title": "Point Mutations in <S0>",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<S0.E.url>",
                    "indexUrl": "<S0.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic"
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "S0.E['udi:use'] == 'point-mutation'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0>.",
        spec=(
                {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<S0.E.url>",
                    "indexUrl": "<S0.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic"
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "S0.E['udi:use'] == 'point-mutation'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Compare with <S0.E> in <S0> at <L>.",
        spec=(
                {
            "title": "Point Mutations in <S0>",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<S0.E.url>",
                    "indexUrl": "<S0.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "S0.E['udi:use'] == 'point-mutation'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <S0.E> in <S0> at <L>.",
        spec=(
                {
            "title": "Point Mutations in <S0> at <L>",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<S0.E.url>",
                    "indexUrl": "<S0.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "S0.E['udi:use'] == 'point-mutation'",
            "S0.E['sample'] == S0['sample']"
        ],
        justification=[
            new_sample,
            new_point
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a view of <E> at <L0>.",
        spec=(
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L0.geneChr>",
                        "interval":["<L0.geneStart>", "<L0.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S['sample'] == S.E['sample']"
        ],
        justification=[
            new_location
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    df = add_row(
        df,
        query_template="Compare with <E> at <L0>.",
        spec=(
            {
            "title": "Point Mutations",
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<L0.geneChr>",
                        "interval":["<L0.geneStart>", "<L0.geneEnd>"]
                    }
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S['sample'] == S.E['sample']"
        ],
        justification=[
            new_location
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    
    # --------------------------------------------------------------------
    # ------------- visual changes ---------------------------------------
    # --------------------------------------------------------------------
    
    circular_view = "The view is circular in accordance with the user's request."
    linear_view = "The view is linear in accordance with the user's request."
    
    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
            {
            "title": "Point Mutations",
            "views": [
                {
                    "layout": "circular",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<E.url>",
                            "indexUrl": "<E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic"
                        },
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "REF",
                            "type": "nominal"
                            },
                            {
                            "field": "ALT",
                            "type": "nominal"
                            }
                        ]
                    }]
                }
                
                
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S['sample'] == S.E['sample']"
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
            {
            "title": "Copy Number Variations",
            "views": [
                {
                    "layout": "circular",
                    "tracks":[{
                        "title": "Copy Number Variants",
                        "data": {
                            "separator": "\t",
                            "url": "<E.url>",
                            "type": "csv",
                            "chromosomeField": "<E.chr1>",
                            "genomicFields": ["<E.start>", "<E.end>"]
                        },
                        "mark": "rect",
                        "x": {
                            "field": "<E.start>",
                            "type": "genomic",
                        },
                        "xe": {
                            "field": "<E.end>",
                            "type": "genomic"
                        },
                        "y": {
                            "field": "total_cn",
                            "type": "quantitative",
                            "axis": "right",
                            "range": [10, 50]
                        },
                    }]
                        
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
             {
                "title": "Structural variants on whole genome",
                "views":[
                    {
                        "layout": "circular",
                        "tracks": [
                        {
                        "data": {
                            "url": "<E.url>",
                            "type": "csv",
                            "separator":"\t",
                            "genomicFieldsToConvert": [
                                {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                                {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                            ]
                        },
                        "mark": "withinLink",
                        "x": {"field": "<E.start1>", "type": "genomic"},
                        "xe": {"field": "<E.end2>", "type": "genomic"},
                        "strokeWidth": {"value": 1},
                        "opacity": {"value": 0.7},
                        "stroke": {"value": "#D55D00"},
                        "style": {"linkStyle": "elliptical"}
                        
                        }
                ]}
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "circular",
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },
                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }]}
            ]
                
                
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == S['sample']"      
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "circular",
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },
                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                        ]
                        
                    }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == S['sample']"     
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> circular.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "circular",
                        "tracks": [
                            {
                                "layout": "linear",
                                "data": {
                                    "url": "<E.url>",
                                    "type": "vector",
                                    "column":"position",
                                    "value":"value"
                                },
                                "mark": "bar",
                                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                                "size": {"value": 2}
                            }
                        ]
                        
                    }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == S['sample']"    
        ],
        justification=[
            circular_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
            {
            "title": "Point Mutations",
            "views": [
                {
                    "layout": "linear",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<E.url>",
                            "indexUrl": "<E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic"
                        },
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "REF",
                            "type": "nominal"
                            },
                            {
                            "field": "ALT",
                            "type": "nominal"
                            }
                        ]
                    }]
                }
                
                
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S['sample'] == S.E['sample']"
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
            {
            "title": "Copy Number Variations",
            "views": [
                {
                    "layout": "linear",
                    "tracks":[{
                        "title": "Copy Number Variants",
                        "data": {
                            "separator": "\t",
                            "url": "<E.url>",
                            "type": "csv",
                            "chromosomeField": "<E.chr1>",
                            "genomicFields": ["<E.start>", "<E.end>"]
                        },
                        "mark": "rect",
                        "x": {
                            "field": "<E.start>",
                            "type": "genomic",
                        },
                        "xe": {
                            "field": "<E.end>",
                            "type": "genomic"
                        },
                        "y": {
                            "field": "total_cn",
                            "type": "quantitative",
                            "axis": "right",
                            "range": [10, 50]
                        },
                    }]
                        
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
             {
                "title": "Structural variants on whole genome",
                "views":[
                    {
                        "layout": "circular",
                        "tracks": [
                        {
                        "data": {
                            "url": "<E.url>",
                            "type": "csv",
                            "separator":"\t",
                            "genomicFieldsToConvert": [
                                {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                                {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                            ]
                        },
                        "mark": "withinLink",
                        "x": {"field": "<E.start1>", "type": "genomic"},
                        "xe": {"field": "<E.end2>", "type": "genomic"},
                        "strokeWidth": {"value": 1},
                        "opacity": {"value": 0.7},
                        "stroke": {"value": "#D55D00"},
                        "style": {"linkStyle": "elliptical"}
                        
                        }
                ]}
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "linear",
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },
                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }]}
            ]
                
                
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == S['sample']"          
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "linear",
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },
                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                        ]
                        
                    }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == S['sample']"     
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Make <E> linear.",
        spec=(
            {
                "title":"<E>",
                "views":[
                    {
                        "layout": "linear",
                        "tracks": [
                            {
                                "layout": "linear",
                                "data": {
                                    "url": "<E.url>",
                                    "type": "vector",
                                    "column":"position",
                                    "value":"value"
                                },
                                "mark": "bar",
                                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                                "size": {"value": 2}
                            }
                        ]
                        
                    }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == S['sample']"    
        ],
        justification=[
            linear_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    # ---------------------------------------------------------------
    # detail views -------------------------------------------------
    # ---------------------------------------------------------------
    # NOTE: Use linking id as detail-1 in the multistep.py code!!!

    detail_view = "A detail view allows for the users to focus on a specific portion of the original plot that may be denser in data."
    general_view = "The whole-genome view allows for the users to see the location-specific view in the context of the whole genome."
    
    # detail view
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            {
                "tracks": [
                    {
                    "data": {
                        "url": "<E.url>",
                        "type": "csv",
                        "separator": "\t",
                        "genomicFieldsToConvert": [
                        {
                            "chromosomeField": "chrom1",
                            "genomicFields": ["start1", "end1"]
                        },
                        {"chromosomeField": "chrom2", "genomicFields": ["start2", "end2"]}
                        ]
                    },
                    "mark": "withinLink",
                    "x": {
                        "field": "<E.start1>",
                        "type": "genomic",
                        "linkingId": "detail-1",
                        "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}
                    },
                    "xe": {"field": "<E.end2>", "type": "genomic"},
                    "color": {"field": "sample", "type": "nominal"},
                    "strokeWidth": {"value": 1},
                    "style": {
                        "background": "blue",
                        "backgroundOpacity": 0.1,
                        "linkStyle": "elliptical"
                    }
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E.url>",
                        "type": "csv",
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start>", "<E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E.start>",
                        "type": "genomic",
                        "linkingId": "detail-1",
                        "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}
                    },
                    "xe": {
                        "field": "<E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                }]
            }
            
            
            
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            
            {
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "linkingId": "detail-1",
                    "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]}
            
            
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "linkingId": "detail-1",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "linkingId": "detail-1",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "linkingId": "detail-1",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a detail view of <E> at <L>.",
        spec=(
            {
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          "linkingId": "detail-1",
                          "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600  
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            detail_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    
    
    # whole-genome view
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
                "tracks": [
                    {
                    "data": {
                        "url": "E.url",
                        "type": "csv",
                        "separator": "\t",

                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                            {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                        ]
                        
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E.start1>", "type": "genomic"},
                    "xe": {"field": "<E.end2>", "type": "genomic"},
                    "color": {"field": "sample", "type": "nominal"},
                    "style": {
                        "linkStyle": "elliptical",
                        "outline": "lightgrey",
                        "outlineWidth": 1,
                        "background": "lightgrey",
                        "backgroundOpacity": 0.2
                    },
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E.url>",
                        "type": "csv",
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start>", "<E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E.start>",
                        "type": "genomic",
                    },
                    "xe": {
                        "field": "<E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }]
            }
            
            
            
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            
            {
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ],
                "alignment": "overlay",
                "tracks": [
                    {"mark": "withinLink"},
                    {
                        "mark": "brush",
                        "x": {"linkingId": "detail-1"},
                        "color": {"value": "blue"}
                    }
                ]
            }]}
            
            
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                "tracks": [
                    {"mark": "withinLink"},
                    {
                        "mark": "brush",
                        "x": {"linkingId": "detail-1"},
                        "color": {"value": "blue"}
                    }
                ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.", 
        spec=({
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      },
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          },
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600,
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ] 
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    # --------------------------------------------------------------------
    # data stratification ------------------------------------------------
    # --------------------------------------------------------------------
    sv_strat = "The SV data is separated by the type of structural variant. This enables ease of veiwing and comparison of location and frequency of different variants across the examination scope."
    point_strat = "The point mutation data is displayed by the mutation type to better visualize the diversity and frequency of different mutations."
    df = add_row(
        df,
        query_template="Stratify the <E> data.",
        spec=(
            {
                "title": "Structural variants on whole genome, by type",
                "tracks": [
                    {
                    "dataTransform": [
                        {
                        "type": "svType",
                        "firstBp": {
                            "chrField": "chrom1",
                            "posField": "start1",
                            "strandField": "strand1"
                        },
                        "secondBp": {
                            "chrField": "chrom2",
                            "posField": "start2",
                            "strandField": "strand2"
                        },
                        "newField": "svclass"
                        },
                        {
                        "type": "replace",
                        "field": "svclass",
                        "replace": [
                            {"from": "DUP", "to": "Duplication"},
                            {"from": "TRA", "to": "Translocation"},
                            {"from": "DEL", "to": "Deletion"},
                            {"from": "t2tINV", "to": "Inversion (TtT)"},
                            {"from": "h2hINV", "to": "Inversion (HtH)"}
                        ],
                        "newField": "svclass"
                        }
                    ],
                    "data": {
                        "url": "<E.url>",
                        "type": "csv",
                        "separator": "\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                            {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "start1", "type": "genomic"},
                    "xe": {"field": "end2", "type": "genomic"},
                    "tooltip": [{"field": "svclass", "type": "nominal"}],
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "row": {
                        "field": "svclass",
                        "type": "nominal",
                        "domain": [
                        "Translocation",
                        "Duplication",
                        "Deletion",
                        "Inversion (TtT)",
                        "Inversion (HtH)"
                        ]
                    },
                    "stroke": {
                        "field": "svclass",
                        "type": "nominal",
                        "legend": True,
                        "domain": [
                        "Translocation",
                        "Duplication",
                        "Deletion",
                        "Inversion (TtT)",
                        "Inversion (HtH)"
                        ],
                        "range": ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
                    },
                    "color": {
                        "field": "svclass",
                        "type": "nominal",
                        "legend": True,
                        "domain": [
                        "Translocation",
                        "Duplication",
                        "Deletion",
                        "Inversion (TtT)",
                        "Inversion (HtH)"
                        ],
                        "range": ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
                    },
                    "style": {"linkStyle": "elliptical"}
                    }
                ]
                }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "E['sample'] == S['sample']"
        ],
        justification=[
            sv_strat
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Stratify the <E> data.",
        spec=({
            "tracks":[{
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic"
                },
                "row": {
                    "field": "SUBTYPE",
                    "type": "nominal",
                    "domain": ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]
                },
                "color": {
                    "field": "SUBTYPE",
                    "type": "nominal",
                    "domain": ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"],
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ]
            }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "E['sample'] == S['sample']"
        ],
        justification=[
            point_strat
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.RECTANGLE,
    )
    
    
    
    # --------------------------------------------------------------------
    # overlays -----------------------------------------------------------
    # --------------------------------------------------------------------
    
    #this could be better phrased 
    atac_overlay = "The atac peaks are overlaid as a line chart. This allows for better comparison of peaks over regions"
    expr_overlay = "The gene expression data is overlaid as a bar chart to allow for better comparison of peaks over regions."
    chip_overlay = "The gene expression data is overlaid as a bar chart to allow for better comparison of peaks over regions."
    sv_overlay = "The structural variant data is overlaid atop the initial visual to allow for direct comparison of variants over regions."
    
    df = add_row(
        df,
        query_template="Overlay <E0>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            expr_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0>.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic"},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )



    df = add_row(
        df,
        query_template="Overlay the <E0> distribution",
        spec=(
            {
            "views":[{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'"
        ],
        justification=[
            expr_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    df = add_row(
        df,
        query_template="Overlay the <E0> distribution",
        spec=(
            {
            "views":[{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'"
        ],
        justification=[
            atac_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay the <E0> distribution",
        spec=(
            {
            "views":[{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'"
        ],
        justification=[
            chip_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    
    
    # overlays @ location
    
    df = add_row(
        df,
        query_template="Overlay <E0> at <L>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'gene expression' or E0['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            expr_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0> at <L>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'atac peaks' or E0['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0> at <L>.",
        spec=(
            {
            "views": [{
            "alignment":"overlay",
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E0.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }]
            }
        ),
        constraints=[
            "E0['format'] == 'bigbed' or E0['format'] == 'bigwig'",
            "E0['udi:use'] == 'peaks' or E0['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Overlay <E0> at <L>.",
        spec=(
            {
                "title": "Structural variants on whole genome",
                "tracks": [
                    {
                    "data": {
                        "url": "<E0.url>",
                        "type": "csv",
                        "separator":"\t",
                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E0.chr1>", "genomicFields":["<E0.start1>", "<E0.end1>"]},
                            {"chromosomeField": "<E0.chr2>", "genomicFields":["<E0.start2>", "<E0.end2>"]},
                        ]
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E0.start1>", "type": "genomic",
                          "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                    "xe": {"field": "<E0.end2>", "type": "genomic"},
                    "strokeWidth": {"value": 1},
                    "opacity": {"value": 0.7},
                    "stroke": {"value": "#D55D00"},
                    "style": {"linkStyle": "elliptical"}
                    
                    }
                ]
            }
        ),
        constraints=[
            "E0['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv_overlay
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    
    
    # overlaying preexisting entities
    df = add_row(
        df,
        query_template="Overlay <E1> and <E2>",
        spec=(
            {
                "title": "<E1> and <E2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "alignment": "overlay",
                    "tracks": [
                        
                        {
                        "id": "track-1",
                        "title": "<E1>",
                        "data": {
                            "url": "<E1.url>",
                            "type": "vcf",
                            "indexUrl": "<E1.index-file>",
                        },
                        
                        "mark": "point",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "domain":
                                {
                                    "chromosome": "chr1",
                                    "interval": [1, 1000000]
                                }
                              },
                        #"y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        },
                    
                        {
                            "data": {
                                "url": "<E2.url>",
                                "type": "csv",
                                "separator":"\t",
                                "genomicFieldsToConvert": [
                                    {"chromosomeField": "<E2.chr1>", "genomicFields":["<E2.start1>", "<E2.end1>"]},
                                    {"chromosomeField": "<E2.chr2>", "genomicFields":["<E2.start2>", "<E2.end2>"]},
                                ]
                            },
                            "mark": "withinLink",
                            "x": {"field": "<E2.start1>", "type": "genomic"},
                            "xe": {"field": "<E2.end2>", "type": "genomic"},
                            "strokeWidth": {"value": 1},
                            "opacity": {"value": 0.7},
                            "stroke": {"value": "#D55D00"},
                            "style": {"linkStyle": "elliptical"}
                            
                        }
                    
                ]
            }]}),
        constraints=[
             "E1['udi:use'] == 'point-mutation'",
             "E2['udi:use'] == 'sv'",  
        ],
        justification=[
            "Point mutations and structural variants are overlaid with one another. This allows for better comparison of different types of variation within the genome. "
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.POINT,
    )
    
    
    df = add_row(
        df,
        query_template="Overlay <E1> and <E2>",
        spec=(
            {
                "title": "<E1> and <E2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "alignment": "overlay",
                    "tracks": [
                        
                        {
                        "id": "track-1",
                        "title": "<E2>",
                        "data": {
                            "url": "<E2.url>",
                            "type": "vcf",
                            "indexUrl": "<E1.index-file>",
                        },
                        
                        "mark": "point",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "domain":
                                {
                                    "chromosome": "chr1",
                                    "interval": [1, 1000000]
                                }
                              },
                        #"y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        },
                    
                        {
                            "data": {
                                "url": "<E2.url>",
                                "type": "csv",
                                "separator":"\t",
                                "genomicFieldsToConvert": [
                                    {"chromosomeField": "<E1.chr1>", "genomicFields":["<E1.start1>", "<E1.end1>"]},
                                    {"chromosomeField": "<E1.chr2>", "genomicFields":["<E1.start2>", "<E1.end2>"]},
                                ]
                            },
                            "mark": "withinLink",
                            "x": {"field": "<E1.start1>", "type": "genomic"},
                            "xe": {"field": "<E1.end2>", "type": "genomic"},
                            "strokeWidth": {"value": 1},
                            "opacity": {"value": 0.7},
                            "stroke": {"value": "#D55D00"},
                            "style": {"linkStyle": "elliptical"}
                            
                        }
                    
                ]
            }]}),
        constraints=[
             "E2['udi:use'] == 'point-mutation'",
             "E1['udi:use'] == 'sv'",  
        ],
        justification=[
            "Point mutations and structural variants are overlaid with one another. This allows for better comparison of different types of variation within the genome. "
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.POINT,
    )
    
    # chipseq, atac set, etc
    df = add_row(
        df,
        query_template="Overlay <E1> and <E2>",
        spec=(
            {
                "title": "<E1> and <E2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "alignment": "overlay",
                    "tracks": [
                        {
                        "layout": "linear",
                        "data": {
                            "url": "<E1.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },
                        "mark": "line",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        },
                        {
                        "layout": "linear",
                        "data": {
                            "url": "<E2.url>",
                            "type": "vector",
                            "column":"position",
                            "value":"value"
                        },
                        "mark": "line",
                        "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                        "y": {"field": "value", "type": "quantitative", "axis": "right"},
                        "size": {"value": 2}
                        }
                    ],  
            }]}),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] == 'atac peaks' or E1['udi:use'] == 'conservative atac peaks' or E1['udi:use'] == 'peaks' or E1['udi:use'] == 'conservative peaks' or E1['udi:use'] == 'gene expression'",
            "E2['udi:use'] == 'atac peaks' or E2['udi:use'] == 'conservative atac peaks' or E2['udi:use'] == 'peaks' or E2['udi:use'] == 'conservative peaks' or E2['udi:use'] == 'gene expression'",
            "E1['udi:use'] != E2['udi:use']",
            "E1['sample'] == E2['sample']",
            "E1['sample'] == S['sample']",
            "E2['sample'] == S['sample']"
        ],
        justification=[
            "Bar and line charts are overlaid with one another. This allows for better comparison of different types of functional signals within the genome. "
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.POINT,
    )


    # --------------------------------------------------------------------------
    # scope ---------------------------------------------------------------
    # --------------------------------------------------------------------------
    df = add_row(
        df,
        query_template="Zoom in on <L0>.",
        spec=(
            {
                "chromosome": "<L0.geneChr>",
                "interval": ["<L0.geneStart>", "<L0.geneEnd>"]
            }
        ),
        constraints=[
        ],
        justification=[
            "The location shifted to the user-specified location from their query."
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    # whole-genome view
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
                "tracks": [
                    {
                    "data": {
                        "url": "E.url",
                        "type": "csv",
                        "separator": "\t",

                        "genomicFieldsToConvert": [
                            {"chromosomeField": "<E.chr1>", "genomicFields":["<E.start1>", "<E.end1>"]},
                            {"chromosomeField": "<E.chr2>", "genomicFields":["<E.start2>", "<E.end2>"]},
                        ]
                        
                    },
                    "mark": "withinLink",
                    "x": {"field": "<E.start1>", "type": "genomic"},
                    "xe": {"field": "<E.end2>", "type": "genomic"},
                    "color": {"field": "sample", "type": "nominal"},
                    "style": {
                        "linkStyle": "elliptical",
                        "outline": "lightgrey",
                        "outlineWidth": 1,
                        "background": "lightgrey",
                        "backgroundOpacity": 0.2
                    },
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            
            {
                "tracks":[{
                    "title": "Copy Number Variants",
                    "data": {
                        "separator": "\t",
                        "url": "<E.url>",
                        "type": "csv",
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start>", "<E.end>"]
                    },
                    "mark": "rect",
                    "x": {
                        "field": "<E.start>",
                        "type": "genomic",
                    },
                    "xe": {
                        "field": "<E.end>",
                        "type": "genomic"
                    },
                    "y": {
                        "field": "total_cn",
                        "type": "quantitative",
                        "axis": "right",
                        "range": [10, 50]
                    },
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }]
            }
            
            
            
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            
            {
            'tracks': [{
                
                "data": {
                    "type": "vcf",
                    "url": "<E.url>",
                    "indexUrl": "<E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                },
                "tooltip": [
                    {
                    "field": "POS",
                    "type": "genomic"
                    },
                    {
                    "field": "REF",
                    "type": "nominal"
                    },
                    {
                    "field": "ALT",
                    "type": "nominal"
                    }
                ],
                "alignment": "overlay",
                "tracks": [
                    {"mark": "withinLink"},
                    {
                        "mark": "brush",
                        "x": {"linkingId": "detail-1"},
                        "color": {"value": "blue"}
                    }
                ]
            }]}
            
            
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            "S.E['sample'] == S['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                "tracks": [
                    {"mark": "withinLink"},
                    {
                        "mark": "brush",
                        "x": {"linkingId": "detail-1"},
                        "color": {"value": "blue"}
                    }
                ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.", 
        spec=({
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [
                {
                "layout": "linear",
                "data": {
                    "url": "<E.url>",
                    "type": "vector",
                    "column":"position",
                    "value":"value"
                },
                "mark": "bar",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      },
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2},
                "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ]
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Add a whole-genome view of <E>.",
        spec=(
            {
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
                        "type": "matrix"
                    },
                    "mark": "bar",
                    "x": {"field": "xs", "type": "genomic", "axis": "top",
                          },
                    "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                    "y": {"field": "ys", "type": "genomic", "axis": "left"},
                    "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                    "color": {"field": "value", "type": "quantitative", "range": "warm"},
                    "width": 600,
                    "height": 600,
                    "alignment": "overlay",
                    "tracks": [
                        {"mark": "withinLink"},
                        {
                            "mark": "brush",
                            "x": {"linkingId": "detail-1"},
                            "color": {"value": "blue"}
                        }
                    ] 
                }]
            }
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            "S.E['sample'] == E['sample']"
        ],
        justification=[
            general_view
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    #print(df)
    return df


if __name__ == "__main__":
    df = generate()
    
    df.to_csv('multistep_generation_test.tsv', sep='\t')
    print(df.head())
