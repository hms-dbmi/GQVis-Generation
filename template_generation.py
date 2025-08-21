import pandas as pd
#from udi_grammar_py import Chart, Op, rolling
from enum import Enum
import json
#import gosling as gos

class QueryType(Enum):
    QUESTION = "question"
    UTTERANCE = "utterance"

class ChartType(Enum):
    IDEOGRAM = "ideogram"
    BARCHART = "barchart"
    POINT = 'point'
    CONNECTIVITY = 'connectivity'
    RECTANGLE = 'rectangle'
    HEATMAP = 'heatmap'
    MULTIVIEW='multiview'
    AREACHART='area chart'
    LINECHART='line chart'
    DETAILVIEW='detail view'

class QueryTaxonomy(Enum):
    LOOKUP = "lookup"
    BROWSE = "browse"
    IDENTIFY = "identify"
    COMPARE_SAMPLE = "sample comparison"
    COMPARE_LOCATIONS = "location comparison"
    COMPARE_ENTITY = "entity comparison"
    COMPARE_METADATA = "metadata comparison"
    SUMMARIZE = "summarize"
    LOCATE = "locate"
    EXPLORE = "explore" 

def add_row(df, query_template, spec, constraints, justification, taxonomy_type: QueryTaxonomy, query_type: QueryType, chart_type: ChartType, caption):
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
        "taxonomy_type": taxonomy_type.value,
        "query_type": query_type.value,
        "creation_method": "template",
        "chart_type": chart_type.value,
        "chart_complexity": complexity,
        "spec_key_count": spec_key_count,
        "justification": justification,
        "caption":caption
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
            "taxonomy_type",
            "creation_method",
            "chart_type",
            "chart_complexity",
            "spec_key_count",
            "justification",
            "caption"
        ]
    )
    
    # ----------- Define caption templates -------------------------------------

    # ----------- Define recurring constraints ---------------------------------
    overlap = "F1['name'] in F2['udi:overlapping_fields'] or F2['udi:overlapping_fields'] == 'all'"
    same_assembly = "S1['udi:assembly'] == S2['udi:assembly']"
    
    different_genes="L1['gene'] != ['gene']"
    different_samples="S1['sample'] != S2['sample']"
    different_entities ="S2.E['url'] != S1.E['url']"

    same_location = "S1.L['gene'] in S2['locations']"
    sample_contains_entity="S1.E['name'] == S2.E['name']"
    entity_in_sample = "S['sample'] == E['sample']"
    entity_in_both_samples = "S1.E['sample'] == S1['sample'] and S2.E['sample'] == S2['sample']"
    entity_three_samples = "E1['sample'] == E2['sample'] == E3['sample']"
    # ----------- Define recurring justifications ------------------------------
    # Visual justifications
    vertical_stacked_view="The plots are stacked vertically to allow for visually-friendly comparison."
    horizontal_stacked_view="The plots are stacked horizontally to allow for visually-friendly comparison."

    matching_zoom="The views are synced to visualize the same genomic region across samples."
    circular_view="A circular view enables a space-condensed visualization across the range of interest."
    detail_view="The detailed view allows for the visualization of specific locations on the main view."
    detail_view_location="The detailed view is centered at the user's specified location."

    # Stratification
    stacked_stratification="The data is split by type between plots to enable comparison across types." + " " + vertical_stacked_view
    color_stratification="The data is colored by type to enable comparison across subtypes."

    # Location zoom
    location_zoom = "The plot's visual scope is centered on the user-defined area of interest."
    whole_genome = "The plot's visual scope covers the full genome, as no location was defined."
    
    # Comparison 
    sample_comparison_vertical = "There are plots for each user-defined sample. " + vertical_stacked_view
    sample_comparison_horizontal = "There are plots for each user-defined sample. " + horizontal_stacked_view

    location_comparison_vertical = "There are plots for each user-defined location. " + vertical_stacked_view
    location_comparison_horizontal = "There are plots for each user-defined location. " + horizontal_stacked_view

    entity_comparison_vertical = "There are plots for each user-defined data comparison. " + vertical_stacked_view
    entity_comparison_horizontal = "There are plots for each user-defined data comparison. " + horizontal_stacked_view

    # Plot type justification
    binned_bars="Bars pool discrete data over genomic ranges to portray the frequency of these discrete data types."
    sv="Structural variant (SV) data is shown in a connectivity plot. The connectivity plot enables viewing of the SV breakpoints between and within chromosomes"
    point_plot="Point marks are used to display the data because the data type is discrete across the genome."
    cnv="Copy number data displays the number of copies in a given sample by elevating the rectangle to the corresponding copy frequency."
    coverage_area="Coverage is displayed in an area plot to convey the depth of reads at each genomic location."
    coverage_line="Coverage is displayed in a line plot to convey the depth of reads at each genomic location."
    coverage_bar="Coverage is displayed in a bar plot to convey the depth of reads at each genomic location."
    
    # 4DN plot type justification
    heatmap="The data is displayed in a heatmap because it highlights the physical contacts between pairs of genomic regions."
    atac_bar="ATAC-seq data is shown as a bar graph to represent chromatin accessibility levels across the genome, with bar height indicating access at each locus."
    atac_area="ATAC-seq data is shown as a area graph to represent chromatin accessibility levels across the genome, with height indicating access at each locus."
    atac_line="ATAC-seq data is shown as a line graph to represent chromatin accessibility levels across the genome, with height indicating access at each locus."
    
    rna_bar="RNA-seq data is shown as a bar graph to represent gene expression levels across the genome, with bar height indicating transcript abundance at each locus."
    rna_area="RNA-seq data is shown as an area graph to represent gene expression levels across the genome, with the area's height indicating transcript abundance at each locus."
    rna_line="RNA-seq data is shown as a line graph to represent gene expression levels across the genome, with line height indicating transcript abundance at each locus."
    chip_bar="ChIP-seq data is shown as a bar graph to represent protein interactions, with bar height corresponding to the frequency of interaction at a given location."
    chip_area="ChIP-seq data is shown as an area graph to represent protein interactions, with the area's height corresponding to the frequency of interaction at a given location."
    chip_line="ChIP-seq data is shown as a line graph to represent protein interactions, with line height corresponding to the frequency of interaction at a given location."
    ideogram="The ideogram portrays the genomic region of interest, providing context for the area of interest. "




    

    
    # --------------------------------------------------------------
    # 4DN Data-based queries ---------------------------------------
    # --------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="What is the <E> data?",
        spec=(
            {
            "title": "Contacts across whole genome",
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
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
            "E['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            heatmap
        ],
        caption="Genomic contact map displaying chromatin interaction frequencies across the genome. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> vary across the genome?",
        spec=(
            {
            "title": "Contacts across whole genome",
            "tracks": [{
                    "data": {
                        "url": "<E.url>",
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
            "E['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            heatmap,
            whole_genome,
        ],
        caption="Genomic contact map displaying chromatin interaction frequencies across the genome. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L>?",
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
            "E['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            heatmap,
            location_zoom
        ],
        caption="Genomic contact map displaying chromatin interaction frequencies at <L>. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> data with an ideogram?",
        spec=(
            
            {
            "title": "HiC with Ideogram",
            "arrangement": "horizontal",
            "spacing": 1,
            "linkingId": "-",
            "views": [
                {
                "spacing": 30,
                "views": [
                    {
                    "spacing": 0,
                    "arrangement": "vertical",
                    "views": [
                        {
                        "xOffset": 30,
                        "tracks": [
                            {
                            "alignment": "overlay",
                            "data": {
                                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.<S.assembly>.Human.CytoBandIdeogram.csv",
                                "type": "csv",
                                "chromosomeField": "Chromosome",
                                "genomicFields": ["chromStart", "chromEnd"]
                            },
                            "tracks": [
                                {
                                "mark": "rect",
                                "dataTransform": [
                                    {
                                    "type": "filter",
                                    "field": "Stain",
                                    "oneOf": ["acen"],
                                    "not": True
                                    }
                                ]
                                },
                                {
                                "mark": "triangleRight",
                                "dataTransform": [
                                    {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
                                    {"type": "filter", "field": "Name", "include": "q"}
                                ]
                                },
                                {
                                "mark": "triangleLeft",
                                "dataTransform": [
                                    {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
                                    {"type": "filter", "field": "Name", "include": "p"}
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
                            "x": {"field": "chromStart", "type": "genomic"},
                            "xe": {"field": "chromEnd", "type": "genomic"},
                            "strokeWidth": {"value": 0},
                            "width": 600,
                            "height": 30
                            }
                        ]
                        },
                        {
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "none"},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {
                                "field": "value",
                                "type": "quantitative",
                                "range": "warm",
                                "legend": True
                            },
                            "width": 600,
                            "height": 600
                            }
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "style": {"outlineWidth": 1, "background": "#F6F6F6"}
            }
            
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            heatmap,
            ideogram
        ],
        caption="Genomic contact map displaying chromatin interaction frequencies across the genome. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains. An ideogram provides contextual location information.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> with an ideogram?",
        spec=(
            
            {
            "title": "Contacts with Ideogram",
            "xDomain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]},
            "arrangement": "horizontal",
            "spacing": 1,
            "linkingId": "-",
            "views": [
                {
                "spacing": 30,
                "views": [
                    {
                    "spacing": 0,
                    "arrangement": "vertical",
                    "views": [
                        {
                        "xOffset": 30,
                        "tracks": [
                            {
                            "alignment": "overlay",
                            "data": {
                                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.<S.assembly>.Human.CytoBandIdeogram.csv",
                                "type": "csv",
                                "chromosomeField": "Chromosome",
                                "genomicFields": ["chromStart", "chromEnd"]
                            },
                            "tracks": [
                                {
                                "mark": "rect",
                                "dataTransform": [
                                    {
                                    "type": "filter",
                                    "field": "Stain",
                                    "oneOf": ["acen"],
                                    "not": True
                                    }
                                ]
                                },
                                {
                                "mark": "triangleRight",
                                "dataTransform": [
                                    {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
                                    {"type": "filter", "field": "Name", "include": "q"}
                                ]
                                },
                                {
                                "mark": "triangleLeft",
                                "dataTransform": [
                                    {"type": "filter", "field": "Stain", "oneOf": ["acen"]},
                                    {"type": "filter", "field": "Name", "include": "p"}
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
                            "x": {"field": "chromStart", "type": "genomic"},
                            "xe": {"field": "chromEnd", "type": "genomic"},
                            "strokeWidth": {"value": 0},
                            "width": 600,
                            "height": 30
                            }
                        ]
                        },
                        {
                        "tracks": [
                            {
                            "data": {
                                "url": "<E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "none",
                                  "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {
                                "field": "value",
                                "type": "quantitative",
                                "range": "warm",
                                "legend": True
                            },
                            "width": 600,
                            "height": 600
                            }
                        ]
                        }
                    ]
                    }
                ]
                }
            ],
            "style": {"outlineWidth": 1, "background": "#F6F6F6"}
            }
            
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            entity_in_sample
        ],
        justification=[
            heatmap,
            ideogram
        ],
        caption="Genomic contact map displaying chromatin interaction frequencies at <L>. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains. An ideogram provides contextual location information.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "Contacts across <L1> and <L2>",
            "arrangement":"horizontal",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Contacts at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "top", 
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {"field": "value", "type": "quantitative", "range": "warm"},
                            "width": 600,
                            "height": 600  
                        }]
                },
                {
                    "tracks":
                        [{
                            "title":"Contacts at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "top", 
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {"field": "value", "type": "quantitative", "range": "warm"},
                            "width": 600,
                            "height": 600  
                        }]
                }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'contact'",
            different_genes,
            entity_in_sample
        ],
        justification=[
            heatmap,
            location_comparison_horizontal
        ],
        caption="Genomic contact maps displaying chromatin interaction frequencies between <L1> and <L2>. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2>?",
        spec=(
            {
            "title": "Contacts across <S1> and <S2>",
            "arrangement":"horizontal",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Contacts at <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                },
                {
                    "tracks":
                        [{
                            "title":"Contacts at <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'contact'",
            "S2.E['udi:use'] == 'contact'",
            different_entities,
            entity_in_both_samples
        ],
        justification=[
            heatmap,
            sample_comparison_horizontal
        ],
        caption="Genomic contact maps displaying chromatin interaction frequencies between <S1> and <S2>. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> at <S1.L.geneName>?",
        spec=(
            {
            "title": "Contacts across <S1> and <S2> at <S1.L.geneName>",
            "arrangement":"horizontal",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Contacts at <S1>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "top",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {"field": "value", "type": "quantitative", "range": "warm"},
                            "width": 600,
                            "height": 600  
                        }]
                },
                {
                    "tracks":
                        [{
                            "title":"Contacts at <S2>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "matrix"
                            },
                            "mark": "bar",
                            "x": {"field": "xs", "type": "genomic", "axis": "top",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "xe": {"field": "xe", "type": "genomic", "axis": "none"},
                            "y": {"field": "ys", "type": "genomic", "axis": "left"},
                            "ye": {"field": "ye", "type": "genomic", "axis": "none"},
                            "color": {"field": "value", "type": "quantitative", "range": "warm"},
                            "width": 600,
                            "height": 600  
                        }]
                }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'contact'",
            "S2.E['udi:use'] == 'contact'",
            different_entities,
            entity_in_both_samples
        ],
        justification=[
            heatmap,
            sample_comparison_horizontal,
            location_zoom
        ],
        caption="Genomic contact maps displaying chromatin interaction frequencies between <S1> and <S2> at <S1.L.geneName>. Warmer colors indicate higher contact frequencies, reflecting regions of spatial proximity, while cooler colors represent lower interaction frequencies. Diagonal enrichment corresponds to local chromosomal interactions, while off-diagonal signals highlight long-range contacts and potential topologically associating domains.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE, 
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
 
    df = add_row(
        df,
        query_template="What is the <E> data?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            whole_genome
        ],
        caption="ChIP-seq signal intensity as a bar chart across genomic loci. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the peaks in the <E>.",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            whole_genome
        ],
        caption="ChIP-seq signal intensity as a bar chart across genomic loci. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_area,
            whole_genome
        ],
        caption="ChIP-seq signal intensity as an area chart across genomic loci. Area height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data as an line chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_line,
            whole_genome
        ],
        caption="ChIP-seq signal intensity as a line chart across genomic loci. Line height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    df = add_row(
        df,
        query_template="What is the distribution of <E>?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            whole_genome
        ],
        caption="Distribution of ChIP-seq signal intensity as a bar chart across genomic loci. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How does <E> vary across the genome?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            whole_genome
        ],
        caption="Distribution of ChIP-seq signal intensity as a bar chart across genomic loci. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L>?",
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
            entity_in_sample
        ],
        justification=[
            chip_bar,
            location_zoom
        ],
        caption="ChIP-seq signal intensity at <L> as a bar chart. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the <E> peaks at <L>.",
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
            entity_in_sample
        ],
        justification=[
            chip_bar,
            location_zoom
        ],
        caption="ChIP-seq signal intensity at <L> as a bar chart. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    df = add_row(
        df,
        query_template="How is <E> distributed at <L>?",
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
            entity_in_sample
        ],
        justification=[
            chip_bar,
            location_zoom
        ],
        caption="Distribution of the ChIP-seq signal intensity. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
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
            entity_in_sample
        ],
        justification=[
            chip_area,
            location_zoom
        ],
        caption="ChIP-seq signal intensity as an area chart. Area height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as a line chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
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
            entity_in_sample
        ],
        justification=[
            chip_line,
            location_zoom
        ],
        caption="ChIP-seq signal intensity at <L> as a line chart. Line height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            location_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <L1> and <L2> as bar charts. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Compare the distribution of <E> at <L1> and <L2>?",
        spec=(
            {
            "title": "Distributin of <E> at <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_bar,
            location_comparison_vertical
        ],
        caption="Distribution of ChIP-seq signal intensity at <L1> and <L2> as bar charts. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_area,
            location_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <L1> and <L2> as area charts. Area height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'peaks' or E['udi:use'] == 'conservative peaks'",
            entity_in_sample
        ],
        justification=[
            chip_line,
            location_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <L1> and <L2> as line charts. line height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2>?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            different_entities,
            "S1.E['udi:use'] == S2.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            chip_bar,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity in <S1> and <S2> as bar charts. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> at <S1.L.geneName>? GOT HERE",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2> at <S1.L.geneName>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            chip_bar,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <S1.L.geneName> in <S1> and <S2> as bar charts. Bar height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="HEREEE How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as an area graph?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            chip_area,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <S1> and <S2> as area charts. Area height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> at <S1.L.geneName> as an area graph?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2> at <S1.L.geneName>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1> at <S1.L.geneName>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2> at <S1.L.geneName>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            chip_area,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <S1.L.geneName> for <S1> and <S2> as area charts. Area height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as a line graph?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            "S1.E['udi:use'] == S1.E['udi:use']",
            different_entities,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
            
        ],
        justification=[
            chip_line,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <S1> and <S2> as line graphs. Line height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> at <S1.L.geneName> as a line graph?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2> at <S1.L.geneName>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1> at <S1.L.geneName>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2> at <S1.L.geneName>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'peaks' or S1.E['udi:use'] == 'conservative peaks'",
            "S1.E['udi:use'] == S1.E['udi:use']",
            different_entities,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
            
        ],
        justification=[
            chip_line,
            sample_comparison_vertical
        ],
        caption="ChIP-seq signal intensity at <S1.L.geneName> in <S1> and <S2> as line graphs. Line height reflects the read coverage or enrichment at each position, indicating regions of protein-DNA binding. Peaks correspond to sites of high occupancy, highlighting potential regulatory elements.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
 
 
 
    df = add_row(
        df,
        query_template="What is the <E> data?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            whole_genome
        ],
        caption="RNA-seq read coverage across genomic loci, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the peaks in <E>.",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression' or E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            whole_genome
        ],
        caption="RNA-seq read coverage across genomic loci, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    
    df = add_row(
        df,
        query_template="What is the <E> data as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_area,
            whole_genome
        ],
        caption="RNA-seq read coverage across genomic loci, illustrating transcription activity. Area height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data as an line chart?",
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
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_line,
            whole_genome
        ],
        caption="RNA-seq read coverage across genomic loci, illustrating transcription activity. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    df = add_row(
        df,
        query_template="What is the distibution of <E>?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            whole_genome
        ],
        caption="Distribution of RNA-seq read coverage across genomic loci, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How does <E> vary across the genome?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            whole_genome
        ],
        caption="Distribution of RNA-seq read coverage across genomic loci, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L>?",
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
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            location_zoom
        ],
        caption="RNA-seq read coverage at <L>, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the <E> peaks at <L>.",
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
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            location_zoom
        ],
        caption="RNA-seq read coverage at <L>, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How is <E> distributed at <L>?",
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
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            location_zoom
        ],
        caption="Distribution of RNA-seq read coverage at <L>, illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_area,
            location_zoom
        ],
        caption="RNA-seq read coverage at <L>, illustrating transcription activity. Area height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as a line chart?",
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
                "mark": "line",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
                      "domain": {"chromosome": "<L.geneChr>", "interval": ["<L.geneStart>", "<L.geneEnd>"]}},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_line,
            location_zoom
        ],
        caption="RNA-seq read coverage at <L>, illustrating transcription activity. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_bar,
            location_comparison_vertical
        ],
        caption="Bar graphs of RNA-seq read coverage at <L1> versus <L2>, illustrating transcription activity. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Compare the distribution of <E> at <L1> and <L2>.",
        spec=(
            {
            "title": "Distributin of <E> at <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample    
            ],
        justification=[
            rna_bar,
            location_comparison_vertical
        ],
        caption="Bar graphs of distribution of RNA-seq read coverage at <L1> versus <L2>, illustrating transcription activity. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_area,
            location_comparison_vertical
        ],
        caption="Area graphs of RNA-seq read coverage at <L1> versus <L2>, illustrating transcription activity. Area height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'gene expression'",
            entity_in_sample
        ],
        justification=[
            rna_line,
            location_comparison_vertical
        ],
        caption="Line graphs of RNA-seq read coverage at <L1> versus <L2>, illustrating transcription activity. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do the positive <E1> and negative <E2> appear?",
        spec=(
            {
            "title": "Postive <E1> and Negative <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Positive <E1>",
                            "data": {
                                "url": "<E1.url>",
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
                {
                    "tracks":
                        [{
                            "title":"Negative <E2>",
                            "data": {
                                "url": "<E2.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] == 'gene expression'",
            "E2['udi:use'] == 'gene expression'",
            "'plus' in E1['name']",
            "'minus' in E2['name']",
            "E1['sample'] == E2['sample']",
        ],
        justification=[
            rna_bar,
            "The plus and minus views are stacked to display positive and negative regulation in conjunction."
        ],
        caption="Positive and negative gene expression rates illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Identify the positive <E1> and negative <E2>.",
        spec=(
            {
            "title": "Postive <E1> and Negative <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Positive <E1>",
                            "data": {
                                "url": "<E1.url>",
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
                {
                    "tracks":
                        [{
                            "title":"Negative <E2>",
                            "data": {
                                "url": "<E2.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] == 'gene expression'",
            "E2['udi:use'] == 'gene expression'",
            "'plus' in E1['name']",
            "'minus' in E2['name']",
            "E1['sample'] == E2['sample']",
        ],
        justification=[
            rna_bar,
            "The plus and minus views are stacked to display positive and negative regulation in conjunction."
        ],
        caption="Positive and negative gene expression rates illustrating transcription activity. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do the positive <E1> and negative expression <E2> appear at <L>?",
        spec=(
            {
            "title": "Postive <E1> and Negative <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Positive <E1>",
                            "data": {
                                "url": "<E1.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom", "domain": {
                                "chromosome": "<L.geneChr>",
                                "interval":["<L.geneStart>", "<L.geneEnd>"]
                                }},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"Negative <E2>",
                            "data": {
                                "url": "<E2.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom","domain": {
                                "chromosome": "<L.geneChr>",
                                "interval":["<L.geneStart>", "<L.geneEnd>"]
                                }},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] == 'gene expression'",
            "E2['udi:use'] == 'gene expression'",
            "'plus' in E1['name']",
            "'minus' in E2['name']",
            "E1['sample'] == E2['sample']"    
        ],
        justification=[
            rna_bar,
            location_zoom,
            "The plus and minus views are stacked to display positive and negative regulation in conjunction."
        ],
        caption="Positive and negative gene expression rates illustrating transcription activity at <L>. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Identify the positive <E1> and negative expression <E2> at <L>.",
        spec=(
            {
            "title": "Postive <E1> and Negative <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"Positive <E1>",
                            "data": {
                                "url": "<E1.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom", "domain": {
                                "chromosome": "<L.geneChr>",
                                "interval":["<L.geneStart>", "<L.geneEnd>"]
                                }},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"Negative <E2>",
                            "data": {
                                "url": "<E2.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom","domain": {
                                "chromosome": "<L.geneChr>",
                                "interval":["<L.geneStart>", "<L.geneEnd>"]
                                }},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] == 'gene expression'",
            "E2['udi:use'] == 'gene expression'",
            "'plus' in E1['name']",
            "'minus' in E2['name']",
            "E1['sample'] == E2['sample']"    
        ],
        justification=[
            rna_bar,
            location_zoom,
            "The plus and minus views are stacked to display positive and negative regulation in conjunction."
        ],
        caption="Positive and negative gene expression rates illustrating transcription activity at <L>. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    
    
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2>?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'gene expression'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            rna_bar,
            sample_comparison_vertical
        ],
        caption="Gene expression rates in <S1> and <S2>. Bar height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as an area chart?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'gene expression'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            rna_area,
            sample_comparison_vertical
        ],
        caption="Gene expression rates in <S1> and <S2>. Area height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as a line chart?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'gene expression'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            rna_line,
            sample_comparison_vertical
        ],
        caption="Gene expression rates in <S1> and <S2>. Line height reflects the number of aligned sequencing reads at each position, with peaks corresponding to exons or regions of high gene expression.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    # atac seq
    
    df = add_row(
        df,
        query_template="What is the <E> data?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_bar,
            whole_genome
        ],
        caption="ATAC-seq read coverage represented as a bar chart across genomic loci. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the peaks in the <E> data.",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_bar,
            whole_genome
        ],
        caption="ATAC-seq read coverage represented as a bar chart across genomic loci. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_area,
            whole_genome
        ],
        caption="ATAC-seq read coverage represented as an area chart across genomic loci. Area height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data as an line chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_line,
            whole_genome
        ],
        caption="ATAC-seq read coverage represented as a line chart across genomic loci. Line height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    df = add_row(
        df,
        query_template="What is the distibution of <E>?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_bar,
            whole_genome
        ],
        caption="Distribution of ATAC-seq read coverage represented as a bar chart across genomic loci. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How does <E> vary across the genome?",
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
                "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                "y": {"field": "value", "type": "quantitative", "axis": "right"},
                "size": {"value": 2}
                }
            ]
            }
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_bar,
            whole_genome
        ],
        caption="Distribution of ATAC-seq read coverage represented as a bar chart across genomic loci. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L>?",
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
            entity_in_sample
        ],
        justification=[
            atac_bar,
            location_zoom
        ],
        caption="ATAC-seq read coverage represented as a bar chart at <L>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Identify the <E> peaks at <L>.",
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
            entity_in_sample
        ],
        justification=[
            atac_bar,
            location_zoom
        ],
        caption="ATAC-seq read coverage represented as a bar chart at <L>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.IDENTIFY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How is <E> distributed at <L>?",
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
            entity_in_sample
        ],
        justification=[
            atac_bar,
            location_zoom
        ],
        caption="ATAC-seq read coverage represented as a bar chart at <L>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as an area chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
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
            entity_in_sample
        ],
        justification=[
            atac_area,
            location_zoom
        ],
        caption="ATAC-seq read coverage represented as an area chart at <L>. Area height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L> as a line chart?",
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
                "mark": "area",
                "x": {"field": "position", "type": "genomic", "axis": "bottom",
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
            entity_in_sample
        ],
        justification=[
            atac_line,
            location_zoom
        ],
        caption="ATAC-seq read coverage represented as a line chart at <L>. Line height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_bar,
            location_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as an bar chart at <L1> and <L2>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Compare the distribution of <E> at <L1> and <L2>.",
        spec=(
            {
            "title": "Distributin of <E> at <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "bar",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
            ],
        justification=[
            atac_bar,
            location_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as an bar chart at <L1> and <L2>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_area,
            location_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as an area chart at <L1> and <L2>. Area height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <E> compare at <L1> and <L2>?",
        spec=(
            {
            "title": "<E> across <L1> and <L2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [{
                            "title":"<E> at <L1>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L1.geneChr>", "interval": ["<L1.geneStart>", "<L1.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [{
                            "title":"<E> at <L2>",
                            "data": {
                                "url": "<E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "line",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom",
                                "domain": {"chromosome": "<L2.geneChr>", "interval": ["<L2.geneStart>", "<L2.geneEnd>"]}},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E['format'] == 'bigbed' or E['format'] == 'bigwig'",
            "E['udi:use'] == 'atac peaks' or E['udi:use'] == 'conservative atac peaks'",
            entity_in_sample
        ],
        justification=[
            atac_line,
            location_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as a line chart at <L1> and <L2>. Line height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2>?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'atac peaks' or S1.E['udi:use'] == 'conservative atac peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            atac_bar,
            sample_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as a bar chart in <S1> and <S2>. Bar height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as an area chart?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
                                "type": "vector",
                                "column":"position",
                                "value":"value"
                            },

                            "mark": "area",
                            "x": {"field": "position", "type": "genomic", "axis": "bottom"},
                            "y": {"field": "value", "type": "quantitative", "axis": "right"},
                            "size": {"value": 2}
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'atac peaks' or S1.E['udi:use'] == 'conservative atac peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            atac_area,
            sample_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as an area chart in <S1> and <S2>. Area height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does the <S1.E> in <S1> compare to the <S2.E> in <S2> as a line chart?",
        spec=(
            {
            "title": "<S1.E> across <S1> and <S2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<S1.E> for <S1>",
                            "data": {
                                "url": "<S1.E.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<S2.E> for <S2>",
                            "data": {
                                "url": "<S2.E.url>",
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
                }
            ]}
        ),
        constraints=[
            "S1.E['format'] == 'bigbed' or S1.E['format'] == 'bigwig'",
            "S1.E['udi:use'] == 'atac peaks' or S1.E['udi:use'] == 'conservative atac peaks'",
            different_entities,
            "S1.E['udi:use'] == S1.E['udi:use']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            atac_line,
            sample_comparison_vertical
        ],
        caption="ATAC-seq read coverage represented as a line chart in <S1> and <S2>. Line height indicates chromatin accessibility, with peaks corresponding to open chromatin regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    
    # display multiple! ------------------------------------------------------------
    df = add_row(
        df,
        query_template="How does <E1> compare with <E2>?",
        spec=(
            {
            "title": "<E1> and <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            
            "E1['udi:use'] != E2['udi:use']",
            "E1['sample'] == E2['sample']",
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. "
        ],
        caption="Sequencing read coverage plotted as a bar chart across genomic loci. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does <E1> compare with <E2> at <L>?",
        spec=(
            {
            "title": "<E1> and <E2>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E1['udi:use'] != E2['udi:use']",
            "E1['sample'] == E2['sample']",
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. ",
            location_zoom
        ],
        caption="Sequencing read coverage plotted as a bar chart at <L>. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <E1>, <E2>, and <E3> compare?",
        spec=(
            {
            "title": "<E1>, <E2>, and <E3>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
                
                {
                    "tracks":
                        [
                            {
                            "title":"<E3>",
                            "data": {
                                "url": "<E3.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E3['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E3['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E1['udi:use'] != E2['udi:use'] and E2['udi:use'] != E3['udi:use'] and E1['udi:use'] != E3['udi:use']",
            entity_three_samples
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. "
        ],
        caption="Sequencing read coverage. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <E1>, <E2>, and <E3> compare at <L>?",
        spec=(
            {
            "title": "<E1>, <E2>, and <E3>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
                },
                
                {
                    "tracks":
                        [
                            {
                            "title":"<E3>",
                            "data": {
                                "url": "<E3.url>",
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
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E3['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E3['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E1['udi:use'] != E2['udi:use'] and E2['udi:use'] != E3['udi:use'] and E1['udi:use'] != E3['udi:use']",
            entity_three_samples
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. ",
            location_zoom
        ],
        caption="Sequencing read coverage at <L>. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment. Heatmap displays contacts between genomic regions.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <E1>, <E2>, and <E3> compare?",
        spec=(
            {
            "title": "<E1>, <E2>, and <E3>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
                
                {
                    "tracks":
                        [
                            {
                                "title":"<E3>",
                                "data": {
                                    "url": "<E3.url>",
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
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E3['udi:use'] in ['contact']",
            "E1['udi:use'] != E2['udi:use'] != E3['udi:use']",
            entity_three_samples
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. "
        ],
        caption="Sequencing read coverage. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment. Heatmap displays contacts between genomic regions. Heatmap represents contacts between genomic regions, with warmer colors suggesting greater contact.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How does <E1>, <E2>, and <E3> compare at <L>?",
        spec=(
            {
            "title": "<E1>, <E2>, and <E3>",
            "arrangement":"vertical",
            "views":[
                {
                    "tracks":
                        [
                            {
                            "title":"<E1>",
                            "data": {
                                "url": "<E1.url>",
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
                },
                {
                    "tracks":
                        [
                            {
                            "title":"<E2>",
                            "data": {
                                "url": "<E2.url>",
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
                },
                
                {
                    "tracks":
                        [
                            {
                                "title":"<E3>",
                                "data": {
                                    "url": "<E3.url>",
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
                            }
                            
                        ]
                }
            ]}
        ),
        constraints=[
            "E1['format'] == 'bigbed' or E1['format'] == 'bigwig'",
            "E2['format'] == 'bigbed' or E2['format'] == 'bigwig'",
            "E1['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E2['udi:use'] in ['atac peaks', 'conservative atac peaks', 'peaks', 'conservative peaks', 'gene expression']",
            "E3['udi:use'] == 'contact'",
            "E1['udi:use'] != E2['udi:use']",
            entity_three_samples
        ],
        justification=[
            entity_comparison_vertical,
            "The visual tracks are selected based on the user inputs. ",
            location_zoom
        ],
        caption="Sequencing read coverage at <L>. Bar height reflects signal intensity at each position, with peaks corresponding to regions of high activity or enrichment. Heatmap displays contacts between genomic regions. Heatmap represents contacts between genomic regions, with warmer colors suggesting greater contact.",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    
    
    

 
    # ---------------------------------------------------------
    #    CHROMOSCOPE DATA
    # ---------------------------------------------------------
    # Mapping entities
    # ---------------------------------------------------------
    
    df = add_row(
        df,
        query_template="What is the <E> data?",
        spec=(
            {
                "title": "Structural variants on whole genome",
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
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            whole_genome
        ],
        caption="Connectivity plot illustrating structural variants (SVs) across the genome. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )

    
    df = add_row(
        df,
        query_template="What is the <E> data in a circular view?",
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
            entity_in_sample
        ],
        justification=[
            sv,
            circular_view,
            whole_genome
        ],
        caption="Connectivity plot illustrating structural variants (SVs) across the genome. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data with a detailed view?",
        spec=(
        
            {
            "title": "Structural Variants",
            "arrangement": "vertical",
            "style": {"enableSmoothPath": True},
            "views": [
                {
                "layout": "circular",
                "spacing": 5,
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
                },
                {
                "layout": "linear",
                "tracks": [
                    {
                    "data": {
                        "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Cervix-AdenoCA/842df341-d34f-4ed6-928c-eaf15bf7f667.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
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
                        "domain": {"chromosome": "chr", "interval": [1, 10000000]}
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
            ]
            }
            
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            detail_view
        ],
        caption="Connectivity plot illustrating structural variants (SVs) across the genome. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.DETAILVIEW,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data with a detailed view at <L>?",
        spec=(
        {
            "title": "Structural Variants",
            "arrangement": "vertical",
            "style": {"enableSmoothPath": True},
            "views": [
                {
                "layout": "circular",
                "spacing": 5,
                "tracks": [
                    {
                    "data": {
                        "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Cervix-AdenoCA/842df341-d34f-4ed6-928c-eaf15bf7f667.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
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
                },
                {
                "layout": "linear",
                "tracks": [
                    {
                    "data": {
                        "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Cervix-AdenoCA/842df341-d34f-4ed6-928c-eaf15bf7f667.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
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
            ]
        }
            
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            detail_view,
            detail_view_location
        ],
        caption="Connectivity plot illustrating structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.DETAILVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="What are <E> at <L>?",
        spec=(
            {
            "title": "Structural variants at <L>",
            "tracks": [
                {
                "data": {
                    "url": "<E.url>",
                    "type": "csv",
                    "separator": "\t",
                    "genomicFieldsToConvert": [
                    {
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start1>", "<E.end1>"]
                    },
                    {
                        "chromosomeField": "<E.chr2>",
                        "genomicFields": ["<E.start2>", "<E.end2>"]
                    }
                    ]
                },
                "mark": "withinLink",
                "x": {
                    "field": "<E.start1>",
                    "type": "genomic",
                    "domain": {
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<E.end2>",
                    "type": "genomic"
                },
                "strokeWidth": {
                    "value": 1
                },
                "opacity": {
                    "value": 0.7
                },
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom,
            entity_in_sample
        ],
        caption="Connectivity plot illustrating structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the frequency of <E> at <L>?",
        spec=(
            {
            "title": "Structural variants at <L>",
            "tracks": [
                {
                "data": {
                    "url": "<E.url>",
                    "type": "csv",
                    "separator": "\t",
                    "genomicFieldsToConvert": [
                    {
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start1>", "<E.end1>"]
                    },
                    {
                        "chromosomeField": "<E.chr2>",
                        "genomicFields": ["<E.start2>", "<E.end2>"]
                    }
                    ]
                },
                "mark": "withinLink",
                "x": {
                    "field": "<E.start1>",
                    "type": "genomic",
                    "domain": {
                    "chromosome": "<L.geneChr>",
                    "interval": ["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<E.end2>",
                    "type": "genomic"
                },
                "strokeWidth": {
                    "value": 1
                },
                "opacity": {
                    "value": 0.7
                },
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Where are the most <E> at <L>?",
        spec=(
            {
            "title": "Structural variants at <L>",
            "tracks": [
                {
                "data": {
                    "url": "<E.url>",
                    "type": "csv",
                    "separator": "\t",
                    "genomicFieldsToConvert": [
                    {
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start1>", "<E.end1>"]
                    },
                    {
                        "chromosomeField": "<E.chr2>",
                        "genomicFields": ["<E.start2>", "<E.end2>"]
                    }
                    ]
                },
                "mark": "withinLink",
                "x": {
                    "field": "<E.start1>",
                    "type": "genomic",
                    "domain": {
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<E.end2>",
                    "type": "genomic"
                },
                "strokeWidth": {
                    "value": 1
                },
                "opacity": {
                    "value": 0.7
                },
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="Where the most <E> in <S> at <L>?",
        spec=(
            {
            "title": "Structural variants at <L> in <S>",
            "tracks": [
                {
                "data": {
                    "url": "<E.url>",
                    "type": "csv",
                    "separator": "\t",
                    "genomicFieldsToConvert": [
                    {
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start1>", "<E.end1>"]
                    },
                    {
                        "chromosomeField": "<E.chr2>",
                        "genomicFields": ["<E.start2>", "<E.end2>"]
                    }
                    ]
                },
                "mark": "withinLink",
                "x": {
                    "field": "<E.start1>",
                    "type": "genomic",
                    "domain": {
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<E.end2>",
                    "type": "genomic"
                },
                "strokeWidth": {
                    "value": 1
                },
                "opacity": {
                    "value": 0.7
                },
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What are <E> at <L> for <S>?",
        spec=(
            {
            "title": "Structural variants at <L> in <S>",
            "tracks": [
                {
                "data": {
                    "url": "<E.url>",
                    "type": "csv",
                    "separator": "\t",
                    "genomicFieldsToConvert": [
                    {
                        "chromosomeField": "<E.chr1>",
                        "genomicFields": ["<E.start1>", "<E.end1>"]
                    },
                    {
                        "chromosomeField": "<E.chr2>",
                        "genomicFields": ["<E.start2>", "<E.end2>"]
                    }
                    ]
                },
                "mark": "withinLink",
                "x": {
                    "field": "<E.start1>",
                    "type": "genomic",
                    "domain": {
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<E.end2>",
                    "type": "genomic"
                },
                "strokeWidth": {
                    "value": 1
                },
                "opacity": {
                    "value": 0.7
                },
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                
                }
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs) at <L>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data, by type?",
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
            entity_in_sample
        ],
        justification=[
            sv,
            whole_genome,
            color_stratification
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs). Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations. Types of structural variant are separated by space and color.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> data at <L>, by type?",
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
                    "x": {"field": "start1", "type": "genomic","domain": {
                            "chromosome": "<L.geneChr>",
                            "interval":["<L.geneStart>", "<L.geneEnd>"]
                        }
                    },
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
            entity_in_sample
        ],
        justification=[
            sv,
            whole_genome,
            color_stratification
        ],
        caption="Connectivity plot illustrating distribution of structural variants (SVs). Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations. Types of structural variant are separated by space and color.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> data?",
        spec=({
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
                    "type": "genomic"
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
                "width": 1400,
                "height": 60
            }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            cnv,
            whole_genome
        ],
        caption="Copy number variation (CNV) profile across the genome. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.RECTANGLE,
    )
    
    
    df = add_row(
        df,
        query_template="What are the <E> at <L>?",
        spec=({
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
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
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
            }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            cnv,
            location_zoom
        ],
        caption="Copy number variation (CNV) profile at <L>. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.RECTANGLE,
    )
    
    df = add_row(
        df,
        query_template="What is the distribution of the <E> on <L>?",
        spec=({
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
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
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
            }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            cnv,
            location_zoom
        ],
        caption="Distribution of copy number variations at <L>. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.RECTANGLE,
    )
    
    df = add_row(
        df,
        query_template="Where are the most <E>?",
        spec=({
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
            }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            cnv,
            location_zoom
        ],
        caption="Copy number variations across loci. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.RECTANGLE,
    )
    
    df = add_row(
        df,
        query_template="Where are the most <E> on <L>?",
        spec=({
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
                    "chromosome": "<L.geneChr>",
                    "interval":["<L.geneStart>", "<L.geneEnd>"]
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
            }
            ]}
        ),
        constraints=[
            "E['udi:use'] == 'cna'",
            entity_in_sample
        ],
        justification=[
            cnv,
            location_zoom
        ],
        caption="Copy number variations at <L>. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.RECTANGLE,
    )
    
    df = add_row(
        df,
        query_template="What are the <E>?",
        spec=({
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
            "E['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            point_plot,
            whole_genome
        ],
        caption="Genomic locations of point mutations across the genome. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.RECTANGLE,
    )
    
    df = add_row(
        df,
        query_template="What are the <E> at <L>?",
        spec=({
            "title": "Point Mutations at <L>",
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
                }],
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            point_plot,
            location_zoom
        ],
        caption="Genomic locations of point mutations at <L>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.POINT,
    )
    
    
    df = add_row(
        df,
        query_template="What are the <E> at <L> in <S>?",
        spec=({
            "title": "Point Mutations at <L> in <S>",
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
                        "chromosome": "<L.geneChr>",
                        "interval": ["<L.geneStart>", "<L.geneEnd>"]
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
                }],
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'",
            entity_in_sample
        ],
        justification=[
            point_plot,
            location_zoom
        ],
        caption="Genomic locations of point mutations at <L>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.POINT,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <E> of the data?",
        spec=(
            {
                "title": "Bar Graph Using BAM Data",
                "layout": "linear",
                "tracks": [
                    {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                        ],
                    "x": {"field": "<E.start>", "type": "genomic"},
                    "xe": {"field": "<E.end>", "type": "genomic"},
                    "y": {"field": "coverage", "type": "quantitative", "axis": "right"},
                    },
                ]     
            }       
        ),
        constraints=[
            "E['udi:use'] == 'coverage'",
            entity_in_sample
        ],
        justification=[
            coverage_bar,
            whole_genome
        ],
        caption="Sequencing read coverage across the genome derived from aligned BAM files. Bar height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> of the data as a line plot?",
        spec=(
            {
                "title": "Bar Graph Using BAM Data",
                "layout": "linear",
                "tracks": [
                    {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                    "mark": "line",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                        ],
                    "x": {"field": "<E.start>", "type": "genomic"},
                    "xe": {"field": "<E.end>", "type": "genomic"},
                    "y": {"field": "coverage", "type": "quantitative", "axis": "right"},
                    },
                ]     
            }       
        ),
        constraints=[
            "E['udi:use'] == 'coverage'",
            entity_in_sample
        ],
        justification=[
            coverage_line,
            whole_genome
        ],
        caption="Sequencing read coverage across the genome derived from aligned BAM files. Line height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINECHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> of the data as an area plot?",
        spec=(
            {
                "title": "Bar Graph Using BAM Data",
                "layout": "linear",
                "tracks": [
                    {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                    "mark": "area",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                        ],
                    "x": {"field": "<E.start>", "type": "genomic"},
                    "xe": {"field": "<E.end>", "type": "genomic"},
                    "y": {"field": "coverage", "type": "quantitative", "axis": "right"},
                    },
                ]     
            }       
        ),
        constraints=[
            "E['udi:use'] == 'coverage'",
            entity_in_sample
        ],
        justification=[
            coverage_area,
            whole_genome
        ],
        caption="Sequencing read coverage across the genome derived from aligned BAM files. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.EXPLORE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREACHART,
    )
        
    df = add_row(
        df,
        query_template="What is the <E> of the data at <L>?",
        spec=(
            {
                "title": "Bar Graph Using BAM Data at <L>",
                "layout": "linear",
                "tracks": [
                    {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                        ],
                    "x": {"field": "<E.start>", "type": "genomic", "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval": ["<L.geneStart>", "<L.geneEnd>"]
                    }},
                    "xe": {"field": "<E.end>", "type": "genomic"},
                    "y": {"field": "coverage", "type": "quantitative", "axis": "right"},
                    },
                ]     
            }       
        ),
        constraints=[
            "E['udi:use'] == 'coverage'",
            entity_in_sample
        ],
        justification=[
            coverage_bar,
            location_zoom
        ],
        caption="Sequencing read coverage <L> derived from aligned BAM files. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the <E> of the data at <L> in <S>?",
        spec=(
            {
                "title": "Coverage Data at <L> in <S>",
                "layout": "linear",
                "tracks": [
                    {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                        ],
                    "x": {"field": "<E.start>", "type": "genomic", "domain": {
                        "chromosome": "<L.geneChr>",
                        "interval": ["<L.geneStart>", "<L.geneEnd>"]
                    }},
                    "xe": {"field": "<E.end>", "type": "genomic"},
                    "y": {"field": "coverage", "type": "quantitative", "axis": "right"},
                    },
                ]     
            }       
        ),
        constraints=[
            "E['udi:use'] == 'coverage'",
            entity_in_sample
        ],
        justification=[
            coverage_bar,
            location_zoom
        ],
        caption="Sequencing read coverage <L> derived from aligned BAM files in <S>. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.LOOKUP,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    
    
    # Analytical queries
    
    df = add_row(
        df,
        query_template="What is the frequency of <E> across <S>?",
        spec=(
            {
                "title": "<E> Frequency",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {"field": "POS", "type": "genomic", "axis": "top"},
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
    
    
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            whole_genome
        ],
        caption="Frequency of point mutations across genomic positions in <S>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.POINT,
    )
    
    df = add_row(
        df,
        query_template="How is <E> distributed in <S>?",
        spec=(
            {
                "title": "<E> Distribution",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {"field": "POS", "type": "genomic", "axis": "top"},
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
    
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            whole_genome
        ],
        caption="Distribution of point mutations across genomic positions in <S>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How is <E> distributed on <L>?",
        spec=(
            {
                "title": "<E> Distribution on <L>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L.geneChr>",
                                    "interval": ["<L.geneStart>", "<L.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            location_zoom
        ],
        caption="Distribution of point mutations across <L>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="How is <E> distributed on <L> in <S>?",
        spec=(
            {
                "title": "<E> Distribution on <L> in <S>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L.geneChr>",
                                    "interval": ["<L.geneStart>", "<L.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            location_zoom
        ],
        caption="Distribution of point mutations across <L> in <S>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="What is the frequency of <E> across <L>?",
        spec=(
            {
                "title": "<E> Frequency on <L>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L.geneChr>",
                                    "interval": ["<L.geneStart>", "<L.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            location_zoom
        ],
        caption="Frequency of point mutations across <L>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.SUMMARIZE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    df = add_row(
        df,
        query_template="Where are the most <S.E> in <L>?",
        spec=(
            {
                "title": "<S.E> on <L>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        {
                        "id": "track-1",
                        "data": {
                            "url": "<S.E.url>",
                            "type": "vcf",
                            "indexUrl": "<S.E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L.geneChr>",
                                    "interval": ["<L.geneStart>", "<L.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    }
                ]
            }
        ),
        constraints=[
            "S.E['udi:use'] == 'point-mutation'", 
            entity_in_sample
        ],
        justification=[
            binned_bars,
            location_zoom
        ],
        caption="Frequency of point mutations across <L>. Bar height indicates the number of observed single nucleotide variants (SNVs) at each locus, highlighting mutational hotspots and regions of elevated variation.",
        taxonomy_type=QueryTaxonomy.LOCATE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
    )
    
    #--------------------------------------------------------------------------
    #Comparative queries
    #--------------------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="How do <E1> and <E2> compare for <S>?",
        spec=(
            {
                "title": "<E1> and <E2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
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
             "E1['sample'] == S['sample']",
             "E2['sample'] == S['sample']"
        ],
        justification=[
            point_plot,
            sv,
            entity_comparison_vertical
        ],
        caption="Comparison of point mutation and structural variant data. Curved links represent SV breakpoints connecting distant loci, while overlaid points indicate SNV locations. ",
        taxonomy_type=QueryTaxonomy.COMPARE_ENTITY,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <E> at <L1> and <L2> compare?",
        spec=(
            {
                "title": "<E> on <L1> and <L2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        
                        {
                        "id": "track-1",
                        "title": "<E> on <L1>",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        
                        "mark": "point",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "domain":
                                {
                                    "chromosome": "<L1.geneChr>",
                                    "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
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
                        }
                    ]
                },
                    {"tracks": [
                        {
                        "id": "track-2",
                        "title": "<E> on <L2>",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "domain":
                                {
                                    "chromosome": "<L2.geneChr>",
                                    "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
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
                        }
                    ]}
                ]
            }
        ),
        constraints=[
             "E['udi:use'] == 'point-mutation'",
             different_genes,
             entity_in_sample
        ],
        justification=[
            point_plot,
            location_comparison_vertical
        ],
        caption="Point mutations at <L1> and <L2>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="Are there more <E> at <L1> or <L2>?",
        spec=(
            {
                "title": "<E> on <L1> and <L2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        
                        {
                        "id": "track-1",
                        "title": "<E> on <L1>",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L1.geneChr>",
                                    "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]
                    },
                    {"tracks": [
                        {
                        "id": "track-2",
                        "title": "<E> on <L2>",
                        "data": {
                            "url": "<E.url>",
                            "type": "vcf",
                            "indexUrl": "<E.index-file>",
                        },
                        "dataTransform": [
                            {
                            "type": "coverage",
                            "startField": "POS",
                            "endField": "POS",
                            "newField": "depth"
                            }
                        ],
                        "mark": "bar",
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L2.geneChr>",
                                    "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ],
                        "opacity": {"value": 1},
                        "width": 600,
                        "height": 130
                        }
                    ]}
                ]
            }
        ),
        constraints=[
             "E['udi:use'] == 'point-mutation'",
             different_genes,
             entity_in_sample
        ],
        justification=[
            point_plot,
            location_comparison_vertical
        ],
        caption="Point mutations at <L1> and <L2>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <E> at <L1> and <L2> compare?",
        spec=(
            {
                "title": "Coverage on <L1> and <L2>",
                "layout": "linear",
                "arrangement": "vertical",
                "centerRadius": 0.8,
                "views": [
                    {
                    "tracks": [
                        
                        {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                        "mark": "bar",
                        "dataTransform": [
                                {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                            ],
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L1.geneChr>",
                                    "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ]
                        },
                        
                        {
                        "data": {
                            "url": "<E.url>",
                            "type": "bam",
                            "indexUrl": "<E.index-file>",
                        },
                        "mark": "bar",
                        "dataTransform": [
                                {"type": "coverage", "startField": "<E.start>", "endField": "<E.end>"}
                            ],
                        
                        
                        "x": {
                            "field": "POS", 
                            "type": "genomic", 
                            "axis": "top",
                            "domain":
                                {
                                    "chromosome": "<L2.geneChr>",
                                    "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
                                }
                              },
                        "y": {"field": "depth", "type": "quantitative"},
                        "tooltip": [
                            {
                            "field": "POS",
                            "type": "genomic"
                            },
                            {
                            "field": "depth",
                            "type": "quantitative"
                            }
                        ]
                        },
                        
                    ]
                    }
                ]
            }
        ),
        constraints=[
             "E['udi:use'] == 'coverage'",
             different_genes,
             entity_in_sample
        ],
        justification=[
            coverage_bar,
            location_comparison_vertical
        ],
        caption="Sequencing read coverage at <L1> and <L2>. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <E> at <L1> and <L2> compare?",
        spec=({
            "title": "Copy Number Variants, <L1> and <L2>",
            "arrangement": "vertical",
            "layout": "linear",
            "views":[
                {
                    "tracks":[
                    {
                        "title":"<L1>",
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
                                "chromosome": "<L1.geneChr>",
                                "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
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
                    }
                    ]
                },
                {
                    "tracks":[
                    {
                        "title":"<L2>",
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
                                "chromosome": "<L2.geneChr>",
                                "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
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
                    }
                    ]
                },
            ]
            }
        ),
        constraints=[
            "E['udi:use'] == 'cna'", 
            different_genes,
            entity_in_sample
        ],
        justification=[
            cnv,
            location_comparison_vertical
        ],
        caption="Copy number variants at <L1> and <L2>. Each rectangle height represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <E> at <L1> and <L2> compare?",
        spec=({
            "title": "Structural Variations, <L1> and <L2>",
            "arrangement": "vertical",
            "layout": "linear",
            "views":
                [
                    {
                        "tracks": [
                        {
                            "title": "<L1>",
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
                            "x": {"field": "<E.start1>", "type": "genomic","domain":{
                                    "chromosome": "<L1.geneChr>",
                                    "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
                                }},
                            "xe": {"field": "<E.end2>", "type": "genomic"},
                            "strokeWidth": {"value": 1},
                            "opacity": {"value": 0.7},
                            "stroke": {"value": "#D55D00"},
                            "style": {"linkStyle": "elliptical"}
                        },]
                    },
                    {"tracks":[{
                        "title": "<L2>",
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
                        "x": {"field": "<E.start1>", "type": "genomic","domain":{
                                "chromosome": "<L2.geneChr>",
                                "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
                            }},
                        "xe": {"field": "<E.end2>", "type": "genomic"},
                        "strokeWidth": {"value": 1},
                        "opacity": {"value": 0.7},
                        "stroke": {"value": "#D55D00"},
                        "style": {"linkStyle": "elliptical"}}
                ]}   
                ]
                
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'", 
            different_genes,
            entity_in_sample
        ],
        justification=[
            sv,
            location_comparison_vertical
        ],
        caption="Connectivity plot illustrating distribution of structural variants at <L1> and <L2>. Curved links connect breakpoints between loci, with arcs representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )    
    
    df = add_row(
        df,
        query_template="How do <E> at <L1> and <L2> compare, by type?",
        spec=(
            {
                "title": "Structural variants on <L1> and <L2>, by type",
                "views": [
                    {
                    "title":"Variants on <L1>",
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
                        "x": {"field": "start1", "type": "genomic", "domain": {
                                "chromosome": "<L1.geneChr>",
                                "interval": ["<L1.geneStart>", "<L1.geneEnd>"]
                                }
                            },
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
                },
                          
                {
                    "title":"Variants on <L2>",
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
                        "x": {"field": "start1", "type": "genomic", "domain": {
                                "chromosome": "<L2.geneChr>",
                                "interval": ["<L2.geneStart>", "<L2.geneEnd>"]
                                }
                            },
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
                }]
                
            }
        ),
        constraints=[
            "E['udi:use'] == 'sv'", 
            "L1['gene'] != L2['gene']",
            entity_in_sample
        ],
        justification=[
            sv,
            location_zoom,
            color_stratification,
            vertical_stacked_view
        ],
        caption="Connectivity plot illustrating distribution of structural variants at <L1> and <L2>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_LOCATIONS,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare at <S1.L.geneName>?",
        spec=({
            "title": "Copy Number Variants, <S1> and <S2>",
            "tracks":[
                {
                "title":"<S1>",
                "data": {
                    "separator": "\t",
                    "url": "<S1.E.url>",
                    "type": "csv",
                    "chromosomeField": "<S1.E.chr1>",
                    "genomicFields": ["<S1.E.start>", "<S1.E.end>"]
                },
                "mark": "rect",
                "x": {
                    "field": "<S1.E.start>",
                    "type": "genomic",
                    "domain": {
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<S1.E.end>",
                    "type": "genomic"
                },
                "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "range": [10, 50]
                  }, 
            },
            {
                "title": "<S2>",
                "data": {
                    "separator": "\t",
                    "url": "<S2.E.url>",
                    "type": "csv",
                    "chromosomeField": "<S2.E.chr1>",
                    "genomicFields": ["<S2.E.start>", "<S2.E.end>"]
                },
                "mark": "rect",
                "x": {
                    "field": "<S2.E.start>",
                    "type": "genomic",
                    "domain":{
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                    }
                },
                "xe": {
                    "field": "<S2.E.end>",
                    "type": "genomic"
                },
                "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "range": [10, 50]
                },
                }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'cna'", 
            "S2.E['udi:use'] == 'cna'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            cnv,
            location_zoom,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Copy number variants in <S1> and <S2> at <S1.L.geneName>. Each rectangle height represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare?",
        spec=({
            "title": "Copy Number Variants, <S1> and <S2>",
            "tracks":[
                {
                "title":"<S1>",
                "data": {
                    "separator": "\t",
                    "url": "<S1.E.url>",
                    "type": "csv",
                    "chromosomeField": "<S1.E.chr1>",
                    "genomicFields": ["<S1.E.start>", "<S1.E.end>"]
                },
                "mark": "rect",
                "x": {
                    "field": "<S1.E.start>",
                    "type": "genomic"
                },
                "xe": {
                    "field": "<S1.E.end>",
                    "type": "genomic"
                },
                "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "range": [10, 50]
                  }, 
            },
            {
                "title": "<S2>",
                "data": {
                    "separator": "\t",
                    "url": "<S2.E.url>",
                    "type": "csv",
                    "chromosomeField": "<S2.E.chr1>",
                    "genomicFields": ["<S2.E.start>", "<S2.E.end>"]
                },
                "mark": "rect",
                "x": {
                    "field": "<S2.E.start>",
                    "type": "genomic"
                },
                "xe": {
                    "field": "<S2.E.end>",
                    "type": "genomic"
                },
                "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "range": [10, 50]
                },
                }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'cna'", 
            "S2.E['udi:use'] == 'cna'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            cnv,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Copy number variants in <S1> and <S2>. Each rectangle height represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare?",
        spec=({
            "title": "Point Mutations, <S1> and <S2>",
            "tracks":[
                {
                "title": "<S1>",
                "data": {
                    "type": "vcf",
                    "url": "<S1.E.url>",
                    "indexUrl": "<S1.E.index-file>",
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
            },
                {
                "title": "<S2>",
                "data": {
                    "type": "vcf",
                    "url": "<S2.E.url>",
                    "indexUrl": "<S2.E.index-file>",
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
            }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'", 
            "S2.E['udi:use'] == 'point-mutation'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Point mutations in <S1> and <S2>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare at <S1.L.geneName>?",
        spec=({
            "title": "Point Mutations, <S1> and <S2>",
            "tracks":[
                {
                "title": "<S1>",
                "data": {
                    "type": "vcf",
                    "url": "<S1.E.url>",
                    "indexUrl": "<S1.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain":{
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
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
            },
                {
                "title": "<S2>",
                "data": {
                    "type": "vcf",
                    "url": "<S2.E.url>",
                    "indexUrl": "<S2.E.index-file>",
                },
                "mark": "point",
                "x": {
                    "field": "POS",
                    "type": "genomic",
                    "domain":{
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
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
            }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'", 
            "S2.E['udi:use'] == 'point-mutation'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            location_zoom,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Point mutations in <S1> and <S2> at <S1.L.geneName>. Each mark indicates the position of a single nucleotide variant.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare?",
        spec=({
            "title": "Structural Variations, <S1> and <S2>",
            "tracks": [
                {
                    "title": "<S1>",
                "data": {
                    "url": "<S1.E.url>",
                    "type": "csv",
                    "separator":"\t",
                    "genomicFieldsToConvert": [
                        {"chromosomeField": "<S1.E.chr1>", "genomicFields":["<S1.E.start1>", "<S1.E.end1>"]},
                        {"chromosomeField": "<S1.E.chr2>", "genomicFields":["<S1.E.start2>", "<S1.E.end2>"]},
                    ]
                },
                "mark": "withinLink",
                "x": {"field": "<S1.E.start1>", "type": "genomic"},
                "xe": {"field": "<S1.E.end2>", "type": "genomic"},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.7},
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                },
                
                {
                    "title": "<S2>",
                "data": {
                    "url": "<S2.E.url>",
                    "type": "csv",
                    "separator":"\t",
                    "genomicFieldsToConvert": [
                        {"chromosomeField": "<S2.E.chr1>", "genomicFields":["<S2.E.start1>", "<S2.E.end1>"]},
                        {"chromosomeField": "<S2.E.chr2>", "genomicFields":["<S2.E.start2>", "<S2.E.end2>"]},
                    ]
                },
                "mark": "withinLink",
                "x": {"field": "<S2.E.start1>", "type": "genomic"},
                "xe": {"field": "<S2.E.end2>", "type": "genomic"},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.7},
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'sv'", 
            "S2.E['udi:use'] == 'sv'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            sv,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1> and <S2>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare at <S1.L.geneName>?",
        spec=({
            "title": "Structural Variations, <S1> and <S2>",
            "tracks": [
                {
                    "title": "<S1>",
                "data": {
                    "url": "<S1.E.url>",
                    "type": "csv",
                    "separator":"\t",
                    "genomicFieldsToConvert": [
                        {"chromosomeField": "<S1.E.chr1>", "genomicFields":["<S1.E.start1>", "<S1.E.end1>"]},
                        {"chromosomeField": "<S1.E.chr2>", "genomicFields":["<S1.E.start2>", "<S1.E.end2>"]},
                    ]
                },
                "mark": "withinLink",
                "x": {"field": "<S1.E.start1>", "type": "genomic","domain":{
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                    }},
                "xe": {"field": "<S1.E.end2>", "type": "genomic"},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.7},
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                },
                
                {
                    "title": "<S2>",
                "data": {
                    "url": "<S2.E.url>",
                    "type": "csv",
                    "separator":"\t",
                    "genomicFieldsToConvert": [
                        {"chromosomeField": "<S2.E.chr1>", "genomicFields":["<S2.E.start1>", "<S2.E.end1>"]},
                        {"chromosomeField": "<S2.E.chr2>", "genomicFields":["<S2.E.start2>", "<S2.E.end2>"]},
                    ]
                },
                "mark": "withinLink",
                "x": {"field": "<S2.E.start1>", "type": "genomic","domain":{
                        "chromosome": "<S1.L.geneChr>",
                        "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                    }},
                "xe": {"field": "<S2.E.end2>", "type": "genomic"},
                "strokeWidth": {"value": 1},
                "opacity": {"value": 0.7},
                "stroke": {"value": "#D55D00"},
                "style": {"linkStyle": "elliptical"}
                }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'sv'", 
            "S2.E['udi:use'] == 'sv'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            sv,
            location_zoom,
            sample_comparison_vertical,
            matching_zoom,
            
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1> and <S2> at <S1.L.geneName>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare at <S1.L.geneName>?",
        spec=({
            "title": "Coverage, <S1> and <S2>",
            "tracks": [
                {
                    "title": "<S1>",
                    "data": {
                        "url": "<S1.E.url>",
                        "type": "bam",
                        "indexUrl": "<S1.E.index-file>",
                    },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<S1.E.start>", "endField": "<S1.E.end>"}
                        ],
                    "x": {
                        "field": "POS", 
                        "type": "genomic", 
                        "axis": "top",
                        "domain":
                            {
                                "chromosome": "<S1.L.geneChr>",
                                "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                            }
                            },
                    "y": {"field": "depth", "type": "quantitative"},
                    "tooltip": [
                        {
                        "field": "POS",
                        "type": "genomic"
                        },
                        {
                        "field": "depth",
                        "type": "quantitative"
                        }
                    ]
                    },
                
                {   
                    "title": "<S2>",
                    "data": {
                        "url": "<S2.E.url>",
                        "type": "bam",
                        "indexUrl": "<S2.E.index-file>",
                    },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<S2.E.start>", "endField": "<S2.E.end>"}
                        ],
                    "x": {
                        "field": "POS", 
                        "type": "genomic", 
                        "axis": "top",
                        "domain":
                            {
                                "chromosome": "<S1.L.geneChr>",
                                "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]
                            }
                            },
                    "y": {"field": "depth", "type": "quantitative"},
                    "tooltip": [
                        {
                        "field": "POS",
                        "type": "genomic"
                        },
                        {
                        "field": "depth",
                        "type": "quantitative"
                        }
                    ]
                    }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'coverage'", 
            "S2.E['udi:use'] == 'coverage'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            coverage_bar,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Sequencing read coverage in <S1> and <S2> at <S1.L.geneName>. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    df = add_row(
        df,
        query_template="How do <S1.E> in <S1> and <S2.E> in <S2> compare?",
        spec=({
            "title": "Coverage, <S1> and <S2>",
            "tracks": [
                {
                    "title": "<S1>",
                    "data": {
                        "url": "<S1.E.url>",
                        "type": "bam",
                        "indexUrl": "<S1.E.index-file>",
                    },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<S1.E.start>", "endField": "<S1.E.end>"}
                        ],
                    "x": {
                        "field": "POS", 
                        "type": "genomic", 
                        "axis": "top",
                        },
                    "y": {"field": "depth", "type": "quantitative"},
                    "tooltip": [
                        {
                        "field": "POS",
                        "type": "genomic"
                        },
                        {
                        "field": "depth",
                        "type": "quantitative"
                        }
                    ]
                    },
                
                {   
                    "title": "<S2>",
                    "data": {
                        "url": "<S2.E.url>",
                        "type": "bam",
                        "indexUrl": "<S2.E.index-file>",
                    },
                    "mark": "bar",
                    "dataTransform": [
                            {"type": "coverage", "startField": "<S2.E.start>", "endField": "<S2.E.end>"}
                        ],
                    "x": {
                        "field": "POS", 
                        "type": "genomic", 
                        "axis": "top"
                        },
                    "y": {"field": "depth", "type": "quantitative"},
                    "tooltip": [
                        {
                        "field": "POS",
                        "type": "genomic"
                        },
                        {
                        "field": "depth",
                        "type": "quantitative"
                        }
                    ]
                    }
            ]}
        ),
        constraints=[
            "S1.E['udi:use'] == 'coverage'", 
            "S2.E['udi:use'] == 'coverage'",
            "S2.E['url'] != S1.E['url']",
            same_assembly,
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            coverage_bar,
            location_zoom,
            sample_comparison_vertical,
            matching_zoom
        ],
        caption="Sequencing read coverage in <S1> and <S2>. Area height reflects the number of reads mapped to each genomic position, with peaks corresponding to regions of high coverage.",
        taxonomy_type=QueryTaxonomy.COMPARE_SAMPLE,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.MULTIVIEW,
    )
    
    # -------------------------------------------------------------------------
    # Metadata-based queries --------------------------------------------------
    # -------------------------------------------------------------------------
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type>?",
        spec=(
            {
                "views":[
                    {
                        "title": "Comparison between SV in <S1.cancer-type> and <S2.cancer-type>",
                        "tracks": [
                            {
                                "title": "<S1.cancer-type>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "csv",
                                "separator":"\t",
                                "genomicFieldsToConvert": [
                                    {"chromosomeField": "<S1.E.chr1>", "genomicFields":["<S1.E.start1>", "<S1.E.end1>"]},
                                    {"chromosomeField": "<S1.E.chr2>", "genomicFields":["<S1.E.start2>", "<S1.E.end2>"]},
                                ]
                            },
                            "mark": "withinLink",
                            "x": {"field": "<S1.E.start1>", "type": "genomic"},
                            "xe": {"field": "<S1.E.end2>", "type": "genomic"},
                            "strokeWidth": {"value": 1},
                            "opacity": {"value": 0.7},
                            "stroke": {"value": "#D55D00"},
                            "style": {"linkStyle": "elliptical"}
                            
                            }]},
                            
                            {
                                "title": "<S2.cancer-type>",
                                "tracks":[
                                {"data": {
                                    "url": "<S2.E.url>",
                                    "type": "csv",
                                    "separator":"\t",
                                    "genomicFieldsToConvert": [
                                        {"chromosomeField": "<S2.E.chr1>", "genomicFields":["<S2.E.start1>", "<S2.E.end1>"]},
                                        {"chromosomeField": "<S2.E.chr2>", "genomicFields":["<S2.E.start2>", "<S2.E.end2>"]},
                                    ]
                                },
                                "mark": "withinLink",
                                "x": {"field": "<S2.E.start1>", "type": "genomic"},
                                "xe": {"field": "<S2.E.end2>", "type": "genomic"},
                                "strokeWidth": {"value": 1},
                                "opacity": {"value": 0.7},
                                "stroke": {"value": "#D55D00"},
                                "style": {"linkStyle": "elliptical"}}
                                ]
                                }
                            
                                   
                        ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'sv'",
            "S2.E['udi:use'] == 'sv'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            sv,
            whole_genome,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1.cancer-type> and <S2.cancer-type>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type>?",
        spec=(
            {
                "views":[
                    
                    {
                    "title": "<S1.cancer-type>",
                    "tracks":[{
                            "data": {
                                "separator": "\t",
                                "url": "<S1.E.url>",
                                "type": "csv",
                                "chromosomeField": "<S1.E.chr1>",
                                "genomicFields": ["<S1.E.start>", "<S1.E.end>"]
                            },
                            "mark": "rect",
                            "x": {
                                "field": "<S1.E.start>",
                                "type": "genomic"
                            },
                            "xe": {
                                "field": "<S1.E.end>",
                                "type": "genomic"
                            },
                            "y": {
                                "field": "total_cn",
                                "type": "quantitative",
                                "axis": "right",
                                "range": [10, 50]
                            },
                            "width": 1400,
                            "height": 60
                        }
                    ]},
                            
                    {
                    "title": "<S2.cancer-type>",
                    "tracks":[{
                            "data": {
                                "separator": "\t",
                                "url": "<S2.E.url>",
                                "type": "csv",
                                "chromosomeField": "<S2.E.chr1>",
                                "genomicFields": ["<S2.E.start>", "<S2.E.end>"]
                            },
                            "mark": "rect",
                            "x": {
                                "field": "<S2.E.start>",
                                "type": "genomic"
                            },
                            "xe": {
                                "field": "<S2.E.end>",
                                "type": "genomic"
                            },
                            "y": {
                                "field": "total_cn",
                                "type": "quantitative",
                                "axis": "right",
                                "range": [10, 50]
                            },
                            "width": 1400,
                            "height": 60
                        }
                        ]}             
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'cna'",
            "S2.E['udi:use'] == 'cna'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            cnv,
            whole_genome,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1.cancer-type> and <S2.cancer-type>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type>?",
        spec=(
            {
                "views":[
                    
                    {
                    "title": "<S1.cancer-type>",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<S1.E.url>",
                            "indexUrl": "<S1.E.index-file>",
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
                    }]},
                            
                    {
                    "title": "<S2.cancer-type>",
                    "tracks":[{
                        "data": {
                            "type": "vcf",
                            "url": "<S2.E.url>",
                            "indexUrl": "<S2.E.index-file>",
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
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'",
            "S2.E['udi:use'] == 'point-mutation'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            whole_genome,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1.cancer-type> and <S2.cancer-type>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type> at <S1.L.geneName>?",
        spec=(
            {
                "views":[
                    {
                        "title": "Comparison between SV in <S1.cancer-type> and <S2.cancer-type>",
                        "tracks": [
                            {
                                "title": "<S1.cancer-type>",
                            "data": {
                                "url": "<S1.E.url>",
                                "type": "csv",
                                "separator":"\t",
                                "genomicFieldsToConvert": [
                                    {"chromosomeField": "<S1.E.chr1>", "genomicFields":["<S1.E.start1>", "<S1.E.end1>"]},
                                    {"chromosomeField": "<S1.E.chr2>", "genomicFields":["<S1.E.start2>", "<S1.E.end2>"]},
                                ]
                            },
                            "mark": "withinLink",
                            "x": {"field": "<S1.E.start1>", "type": "genomic",
                                  "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                            "xe": {"field": "<S1.E.end2>", "type": "genomic"},
                            "strokeWidth": {"value": 1},
                            "opacity": {"value": 0.7},
                            "stroke": {"value": "#D55D00"},
                            "style": {"linkStyle": "elliptical"}
                            
                            }]},
                            
                            {
                                "title": "<S2.cancer-type>",
                                "tracks":[
                                {"data": {
                                    "url": "<S2.E.url>",
                                    "type": "csv",
                                    "separator":"\t",
                                    "genomicFieldsToConvert": [
                                        {"chromosomeField": "<S2.E.chr1>", "genomicFields":["<S2.E.start1>", "<S2.E.end1>"]},
                                        {"chromosomeField": "<S2.E.chr2>", "genomicFields":["<S2.E.start2>", "<S2.E.end2>"]},
                                    ]
                                },
                                "mark": "withinLink",
                                "x": {"field": "<S2.E.start1>", "type": "genomic",
                                      "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}},
                                "xe": {"field": "<S2.E.end2>", "type": "genomic"},
                                "strokeWidth": {"value": 1},
                                "opacity": {"value": 0.7},
                                "stroke": {"value": "#D55D00"},
                                "style": {"linkStyle": "elliptical"}}
                                ]
                                }
                            
                                   
                        ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'sv'",
            "S2.E['udi:use'] == 'sv'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            sv,
            location_zoom,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Connectivity plot illustrating distribution of structural variants in <S1.cancer-type> and <S2.cancer-type> at <S1.L.geneName>. Curved links connect breakpoints between loci, with different colors representing deletions, duplications, inversions, or translocations.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type>?",
        spec=(
            {
                "views":[
                    
                    {
                    "title": "<S1.cancer-type>",
                    "tracks":[{
                            "data": {
                                "separator": "\t",
                                "url": "<S1.E.url>",
                                "type": "csv",
                                "chromosomeField": "<S1.E.chr1>",
                                "genomicFields": ["<S1.E.start>", "<S1.E.end>"]
                            },
                            "mark": "rect",
                            "x": {
                                "field": "<S1.E.start>",
                                "type": "genomic",                                
                            },
                            "xe": {
                                "field": "<S1.E.end>",
                                "type": "genomic"
                            },
                            "y": {
                                "field": "total_cn",
                                "type": "quantitative",
                                "axis": "right",
                                "range": [10, 50]
                            },
                            "width": 1400,
                            "height": 60
                        }
                    ]},
                            
                    {
                    "title": "<S2.cancer-type>",
                    "tracks":[{
                            "data": {
                                "separator": "\t",
                                "url": "<S2.E.url>",
                                "type": "csv",
                                "chromosomeField": "<S2.E.chr1>",
                                "genomicFields": ["<S2.E.start>", "<S2.E.end>"]
                            },
                            "mark": "rect",
                            "x": {
                                "field": "<S2.E.start>",
                                "type": "genomic"
                            },
                            "xe": {
                                "field": "<S2.E.end>",
                                "type": "genomic"
                            },
                            "y": {
                                "field": "total_cn",
                                "type": "quantitative",
                                "axis": "right",
                                "range": [10, 50]
                            },
                            "width": 1400,
                            "height": 60
                        }
                        ]}             
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'cna'",
            "S2.E['udi:use'] == 'cna'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            cnv,
            location_zoom,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Copy number variation (CNV) profile in <S1.cancer-type> and <S2.cancer-type>. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cancer-type> versus the <S2.E> data in <S2> with <S2.cancer-type> at <S1.L.geneName>?",
        spec=(
            {
                "views":[
                    
                    {
                    "title": "<S1.cancer-type>",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<S1.E.url>",
                            "indexUrl": "<S1.E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic",
                            "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}
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
                    }]},
                            
                    {
                    "title": "<S2.cancer-type>",
                    "tracks":[{
                        "data": {
                            "type": "vcf",
                            "url": "<S2.E.url>",
                            "indexUrl": "<S2.E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic",
                            "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}
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
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'",
            "S2.E['udi:use'] == 'point-mutation'",
            "S1['udi:cancer-type'] != S2['udi:cancer-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            location_zoom,
            "This diagram compares two cancer types, stacking them vertically for viewing ease."
        ],
        caption="Copy number variation (CNV) profile in <S1.cancer-type> and <S2.cancer-type> in <S1.L.geneName>. Each point represents the measured copy number at a genomic locus, with deviations above or below the baseline diploid state indicating amplifications or deletions.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    
    
    # cell types
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cell-type> versus the <S2.E> data in <S2> with <S2.cell-type>?",
        spec=(
            {
                "views":[                    
                    {
                    "title": "<S1.cell-type>",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<S1.E.url>",
                            "indexUrl": "<S1.E.index-file>",
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
                    }]},
                            
                    {
                    "title": "<S2.cell-type>",
                    "tracks":[{
                        "data": {
                            "type": "vcf",
                            "url": "<S2.E.url>",
                            "indexUrl": "<S2.E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic",
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
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'",
            "S2.E['udi:use'] == 'point-mutation'",
            "S1['udi:cell-type'] != S2['udi:cell-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            location_zoom,
            "This diagram compares two cell types, stacking them vertically for viewing ease."
        ],
        caption="Point mutation profile profile in <S1.cell-type> and <S2.cell-type>. Each point represents a single nucleotide variation.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )
    
    df = add_row(
        df,
        query_template="What is the <S1.E> data in <S1> with <S1.cell-type> versus the <S2.E> data in <S2> with <S2.cell-type> at <S1.L.geneName>?",
        spec=(
            {
                "views":[                    
                    {
                    "title": "<S1.cell-type>",
                    'tracks': [{
                        "data": {
                            "type": "vcf",
                            "url": "<S1.E.url>",
                            "indexUrl": "<S1.E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic",
                            "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}
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
                    }]},
                            
                    {
                    "title": "<S2.cell-type>",
                    "tracks":[{
                        "data": {
                            "type": "vcf",
                            "url": "<S2.E.url>",
                            "indexUrl": "<S2.E.index-file>",
                        },
                        "mark": "point",
                        "x": {
                            "field": "POS",
                            "type": "genomic",
                            "domain": {"chromosome": "<S1.L.geneChr>", "interval": ["<S1.L.geneStart>", "<S1.L.geneEnd>"]}
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
                ]
       
            }
            
        ),
        constraints=[
            "S1.E['udi:use'] == 'point-mutation'",
            "S2.E['udi:use'] == 'point-mutation'",
            "S1['udi:cell-type'] != S2['udi:cell-type']",
            "S1.E['sample'] == S1['sample']",
            "S2.E['sample'] == S2['sample']"
        ],
        justification=[
            point_plot,
            location_zoom,
            "This diagram compares two cell types, stacking them vertically for viewing ease."
        ],
        caption="Point mutation profile profile in <S1.cell-type> and <S2.cell-type> in <S1.L.geneName>. Each point represents a single nucleotide variation.",
        taxonomy_type=QueryTaxonomy.COMPARE_METADATA,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CONNECTIVITY,
    )

    return df


if __name__ == "__main__":
    df = generate()
    
    df.to_csv('spec_generation_test.tsv', sep='\t')
    print(df.head())
