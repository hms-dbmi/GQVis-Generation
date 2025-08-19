df = add_row(
        df,
        query_template="Browse the structural data.",
        spec=(
            
            {
  "layout": "linear",
  "arrangement": "vertical",
  "centerRadius": 0.5,
  "assembly": "hg19",
  "spacing": 40,
  "style": {
    "outlineWidth": 1,
    "outline": "lightgray",
    "enableSmoothPath": False
  },
  "views": [
    {
      "arrangement": "vertical",
      "views": [
        {
          "xOffset": 560,
          "static": True,
          "layout": "circular",
          "spacing": 1,
          "style": {
            "outlineWidth": 1,
            "outline": "lightgray"
          },
          "tracks": [
            {
              "title": "Ideogram",
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-top-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
                "type": "csv",
                "chromosomeField": "Chromosome",
                "genomicFields": [
                  "chromStart",
                  "chromEnd"
                ]
              },
              "tracks": [
                {
                  "mark": "rect"
                },
                {
                  "mark": "brush",
                  "x": {
                    "linkingId": "mid-scale"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "stroke": {
                    "value": "#0070DC"
                  },
                  "color": {
                    "value": "#AFD8FF"
                  },
                  "opacity": {
                    "value": 0.5
                  }
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 600,
              "height": 100
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-top-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/5bc448e3-ad54-47be-beb9-aec2b983bf5f",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 10
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 600,
              "height": 40
            },
            {
              "id": "driver-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-top-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "gain-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-top-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "loh-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-top-sv",
              "title": "",
              "alignment": "overlay",
              
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                }
              ],
              "y": {
                "value": 16
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 600,
              "height": 80
            }
          ]
        },
        {
          "linkingId": "mid-scale",
          "xDomain": {
            "chromosome": "chr1"
          },
          "layout": "linear",
          "tracks": [
            {
              "title": "Ideogram",
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 1720,
              "height": 18
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/67f6af1a-1d10-413a-a38e-f337fdb9730b",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 14
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 40
            },
            {
              "id": "driver-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-gene",
              "title": "  Gene Annotation",
              "template": "gene",
              "data": {
                "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation-hg19",
                "type": "beddb",
                "genomicFields": [
                  {
                    "index": 1,
                    "name": "start"
                  },
                  {
                    "index": 2,
                    "name": "end"
                  }
                ],
                "valueFields": [
                  {
                    "index": 5,
                    "name": "strand",
                    "type": "nominal"
                  },
                  {
                    "index": 3,
                    "name": "name",
                    "type": "nominal"
                  }
                ],
                "exonIntervalFields": [
                  {
                    "index": 12,
                    "name": "start"
                  },
                  {
                    "index": 13,
                    "name": "end"
                  }
                ]
              },
              "encoding": {
                "startPosition": {
                  "field": "start"
                },
                "endPosition": {
                  "field": "end"
                },
                "strandColor": {
                  "field": "strand",
                  "range": [
                    "gray"
                  ]
                },
                "strandRow": {
                  "field": "strand"
                },
                "opacity": {
                  "value": 0.4
                },
                "geneHeight": {
                  "value": 20
                },
                "geneLabel": {
                  "field": "name"
                },
                "geneLabelFontSize": {
                  "value": 20
                },
                "geneLabelColor": {
                  "field": "strand",
                  "range": [
                    "black"
                  ]
                },
                "geneLabelStroke": {
                  "value": "white"
                },
                "geneLabelStrokeThickness": {
                  "value": 4
                },
                "geneLabelOpacity": {
                  "value": 1
                },
                "type": {
                  "field": "type"
                }
              },
              "tooltip": [
                {
                  "field": "name",
                  "type": "nominal"
                },
                {
                  "field": "strand",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 60
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-mutation",
              "title": "  Point Mutation",
              "style": {
                "background": "#FFFFFF",
                "inlineLegend": True
              },
              "data": {
                "type": "vcf",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.sorted.vcf.gz.tbi",
                "sampleLength": 500
              },
              "alignment": "overlay",
              "dataTransform": [
                {
                  "field": "DISTPREV",
                  "type": "filter",
                  "oneOf": [0],
                  "not": True
                }
              ],
              "tracks": [
                {
                  "dataTransform": [
                    {
                      "field": "DISTPREV",
                      "type": "filter",
                      "oneOf": [0],
                      "not": True
                    }
                  ]
                },
                {
                  "dataTransform": [
                    {
                      "field": "POS",
                      "type": "filter",
                      "oneOf": []
                    }
                  ],
                  "stroke": {
                    "field": "SUBTYPE",
                    "type": "nominal",
                    "legend": True,
                    "domain": [
                      "C\u003EA",
                      "C\u003EG",
                      "C\u003ET",
                      "T\u003EA",
                      "T\u003EC",
                      "T\u003EG"
                    ]
                  },
                  "strokeWidth": {
                    "value": 10
                  },
                  "opacity": {
                    "value": 0.3
                  }
                }
              ],
              "mark": "point",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "SUBTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "C\u003EA",
                  "C\u003EG",
                  "C\u003ET",
                  "T\u003EA",
                  "T\u003EC",
                  "T\u003EG"
                ]
              },
              "y": {
                "field": "DISTPREVLOGE",
                "type": "quantitative",
                "axis": "right",
                "range": [10, 50]
              },
              "opacity": {
                "value": 0.9
              },
              "tooltip": [
                {
                  "field": "DISTPREV",
                  "type": "nominal",
                  "format": "s1",
                  "alt": "Distance To Previous Mutation (BP)"
                },
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "SUBTYPE",
                  "type": "nominal"
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
              "width": 1720,
              "height": 60
            },
            {
              "id": "mutation-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-indel",
              "title": "  Indel",
              "style": {
                "background": "#F6F6F6",
                "inlineLegend": True
              },
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20161006.somatic.indel.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20161006.somatic.indel.sorted.vcf.gz.tbi",
                "type": "vcf",
                "sampleLength": 500
              },
              "dataTransform": [
                {
                  "type": "concat",
                  "fields": [
                    "REF",
                    "ALT"
                  ],
                  "separator": " → ",
                  "newField": "LAB"
                },
                {
                  "type": "replace",
                  "field": "MUTTYPE",
                  "replace": [
                    {
                      "from": "insertion",
                      "to": "Insertion"
                    },
                    {
                      "from": "deletion",
                      "to": "Deletion"
                    }
                  ],
                  "newField": "MUTTYPE"
                }
              ],
              "alignment": "overlay",
              "tracks": [
                {
                  "size": {
                    "value": 19
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "GT",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                },
                {
                  "xe": {
                    "field": "POSEND",
                    "type": "genomic",
                    "axis": "top"
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "LTET",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "row": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "tooltip": [
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "POSEND",
                  "type": "genomic"
                },
                {
                  "field": "MUTTYPE",
                  "type": "nominal"
                },
                {
                  "field": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "REF",
                  "type": "nominal"
                },
                {
                  "field": "QUAL",
                  "type": "quantitative"
                }
              ],
              "opacity": {
                "value": 0.9
              },
              "width": 1720,
              "height": 40
            },
            {
              "id": "indel-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-cnv",
              "title": "  Copy Number Variants",
              "style": {
                "background": "#FFFFFF"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "alignment": "overlay",
              "tracks": [
                {
                  "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "grid": True,
                    "range": [10, 50]
                  },
                  "color": {
                    "value": "#808080"
                  }
                }
              ],
              "tooltip": [
                {
                  "field": "total_cn",
                  "type": "quantitative"
                },
                {
                  "field": "major_cn",
                  "type": "quantitative"
                },
                {
                  "field": "minor_cn",
                  "type": "quantitative"
                }
              ],
              "size": {
                "value": 5
              },
              "stroke": {
                "value": "#808080"
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "width": 1720,
              "height": 60
            },
            {
              "id": "cnv-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "gain-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "loh-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "aff5793b-3197-4d1d-bf0a-9b0ded5f2937-mid-sv",
              "title": "  Structural Variants",
              "alignment": "overlay",
              
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/aff5793b-3197-4d1d-bf0a-9b0ded5f2937.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                }
              ],
              "y": {
                "value": 50
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 1720,
              "height": 250
            }
          ]
        }
      ]
    }
  ]
}
            
        ),
        constraints=[
        ],
        justification=[
            "This visual comes from the Chromoscope visualization database."
        ],
        caption="Integrative visualization of genomic alterations across the human genome. A circos plot (top) depicts structural variants, including translocations, duplications, deletions, and inversions, across chromosomes. Inner tracks indicate regions of copy number gain, loss of heterozygosity (LOH), and putative driver events. The expanded linear view (bottom) shows chromosome 1 in detail, with ideogram, annotated genes, point mutations stratified by substitution class, indels, and copy number variants. Together, these tracks highlight the co-occurrence of single-nucleotide variants, indels, and large-scale structural rearrangements in the context of chromosomal architecture.",
        taxonomy_type=QueryTaxonomy.BROWSE,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.MULTIVIEW,
    )


df = add_row(
        df,
        query_template="Browse the structural data.",
        spec=(
        
        ​​{
  "layout": "linear",
  "arrangement": "vertical",
  "centerRadius": 0.5,
  "assembly": "hg19",
  "spacing": 40,
  "style": {
    "outlineWidth": 1,
    "outline": "lightgray",
    "enableSmoothPath": False
  },
  "views": [
    {
      "arrangement": "vertical",
      "views": [
        {
          "xOffset": 560,
          "static": True,
          "layout": "circular",
          "spacing": 1,
          "style": {
            "outlineWidth": 1,
            "outline": "lightgray"
          },
          "tracks": [
            {
              "title": "Ideogram",
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-top-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
                "type": "csv",
                "chromosomeField": "Chromosome",
                "genomicFields": [
                  "chromStart",
                  "chromEnd"
                ]
              },
              "tracks": [
                {
                  "mark": "rect"
                },
                {
                  "mark": "brush",
                  "x": {
                    "linkingId": "mid-scale"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "stroke": {
                    "value": "#0070DC"
                  },
                  "color": {
                    "value": "#AFD8FF"
                  },
                  "opacity": {
                    "value": 0.5
                  }
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 600,
              "height": 100
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-top-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/36fb778c-41c8-47e2-b498-dd8cf497d527",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 10
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 600,
              "height": 40
            },
            {
              "id": "driver-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-top-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "gain-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-top-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "loh-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-top-sv",
              "title": "",
              "alignment": "overlay",
              
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                }
              ],
              "y": {
                "value": 16
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 600,
              "height": 80
            }
          ]
        },
        {
          "linkingId": "mid-scale",
          "xDomain": {
            "chromosome": "chr1"
          },
          "layout": "linear",
          "tracks": [
            {
              "title": "  Ideogram",
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 1720,
              "height": 18
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/84bc26fe-04b2-4c46-8d51-1e3eb80e2cd2",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 14
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 40
            },
            {
              "id": "driver-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-gene",
              "title": "  Gene Annotation",
              "template": "gene",
              "data": {
                "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation-hg19",
                "type": "beddb",
                "genomicFields": [
                  {
                    "index": 1,
                    "name": "start"
                  },
                  {
                    "index": 2,
                    "name": "end"
                  }
                ],
                "valueFields": [
                  {
                    "index": 5,
                    "name": "strand",
                    "type": "nominal"
                  },
                  {
                    "index": 3,
                    "name": "name",
                    "type": "nominal"
                  }
                ],
                "exonIntervalFields": [
                  {
                    "index": 12,
                    "name": "start"
                  },
                  {
                    "index": 13,
                    "name": "end"
                  }
                ]
              },
              "encoding": {
                "startPosition": {
                  "field": "start"
                },
                "endPosition": {
                  "field": "end"
                },
                "strandColor": {
                  "field": "strand",
                  "range": [
                    "gray"
                  ]
                },
                "strandRow": {
                  "field": "strand"
                },
                "opacity": {
                  "value": 0.4
                },
                "geneHeight": {
                  "value": 20
                },
                "geneLabel": {
                  "field": "name"
                },
                "geneLabelFontSize": {
                  "value": 20
                },
                "geneLabelColor": {
                  "field": "strand",
                  "range": [
                    "black"
                  ]
                },
                "geneLabelStroke": {
                  "value": "white"
                },
                "geneLabelStrokeThickness": {
                  "value": 4
                },
                "geneLabelOpacity": {
                  "value": 1
                },
                "type": {
                  "field": "type"
                }
              },
              "tooltip": [
                {
                  "field": "name",
                  "type": "nominal"
                },
                {
                  "field": "strand",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 60
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-mutation",
              "title": "  Point Mutation",
              "style": {
                "background": "#FFFFFF",
                "inlineLegend": True
              },
              "data": {
                "type": "vcf",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.sorted.vcf.gz.tbi",
                "sampleLength": 500
              },
              "alignment": "overlay",
              "dataTransform": [
                {
                  "field": "DISTPREV",
                  "type": "filter",
                  "oneOf": [0],
                  "not": True
                }
              ],
              "tracks": [
                {
                  "dataTransform": [
                    {
                      "field": "DISTPREV",
                      "type": "filter",
                      "oneOf": [0],
                      "not": True
                    }
                  ]
                },
                {
                  "dataTransform": [
                    {
                      "field": "POS",
                      "type": "filter",
                      "oneOf": [null]
                    }
                  ],
                  "stroke": {
                    "field": "SUBTYPE",
                    "type": "nominal",
                    "legend": True,
                    "domain": [
                      "C\u003EA",
                      "C\u003EG",
                      "C\u003ET",
                      "T\u003EA",
                      "T\u003EC",
                      "T\u003EG"
                    ]
                  },
                  "strokeWidth": {
                    "value": 10
                  },
                  "opacity": {
                    "value": 0.3
                  }
                }
              ],
              "mark": "point",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "SUBTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "C\u003EA",
                  "C\u003EG",
                  "C\u003ET",
                  "T\u003EA",
                  "T\u003EC",
                  "T\u003EG"
                ]
              },
              "y": {
                "field": "DISTPREVLOGE",
                "type": "quantitative",
                "axis": "right",
                "range": [10, 50]
              },
              "opacity": {
                "value": 0.9
              },
              "tooltip": [
                {
                  "field": "DISTPREV",
                  "type": "nominal",
                  "format": "s1",
                  "alt": "Distance To Previous Mutation (BP)"
                },
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "SUBTYPE",
                  "type": "nominal"
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
              "width": 1720,
              "height": 60
            },
            {
              "id": "mutation-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-indel",
              "title": "  Indel",
              "style": {
                "background": "#F6F6F6",
                "inlineLegend": True
              },
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20161006.somatic.indel.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20161006.somatic.indel.sorted.vcf.gz.tbi",
                "type": "vcf",
                "sampleLength": 500
              },
              "dataTransform": [
                {
                  "type": "concat",
                  "fields": [
                    "REF",
                    "ALT"
                  ],
                  "separator": " → ",
                  "newField": "LAB"
                },
                {
                  "type": "replace",
                  "field": "MUTTYPE",
                  "replace": [
                    {
                      "from": "insertion",
                      "to": "Insertion"
                    },
                    {
                      "from": "deletion",
                      "to": "Deletion"
                    }
                  ],
                  "newField": "MUTTYPE"
                }
              ],
              "alignment": "overlay",
              "tracks": [
                {
                  "size": {
                    "value": 19
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "GT",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                },
                {
                  "xe": {
                    "field": "POSEND",
                    "type": "genomic",
                    "axis": "top"
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "LTET",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "row": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "tooltip": [
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "POSEND",
                  "type": "genomic"
                },
                {
                  "field": "MUTTYPE",
                  "type": "nominal"
                },
                {
                  "field": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "REF",
                  "type": "nominal"
                },
                {
                  "field": "QUAL",
                  "type": "quantitative"
                }
              ],
              "opacity": {
                "value": 0.9
              },
              "width": 1720,
              "height": 40
            },
            {
              "id": "indel-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-cnv",
              "title": "  Copy Number Variants",
              "style": {
                "background": "#FFFFFF"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "alignment": "overlay",
              "tracks": [
                {
                  "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "grid": True,
                    "range": [10, 50]
                  },
                  "color": {
                    "value": "#808080"
                  }
                }
              ],
              "tooltip": [
                {
                  "field": "total_cn",
                  "type": "quantitative"
                },
                {
                  "field": "major_cn",
                  "type": "quantitative"
                },
                {
                  "field": "minor_cn",
                  "type": "quantitative"
                }
              ],
              "size": {
                "value": 5
              },
              "stroke": {
                "value": "#808080"
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "width": 1720,
              "height": 60
            },
            {
              "id": "cnv-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "gain-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "loh-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "4ceeb025-2f16-4f80-b9b4-0151346349c6-mid-sv",
              "title": "  Structural Variants",
              "alignment": "overlay",
              
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/4ceeb025-2f16-4f80-b9b4-0151346349c6.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                }
              ],
              "y": {
                "value": 50
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 1720,
              "height": 250
            }
          ]
        }
      ]
    }
  ]
}


            
            
        ),
        constraints=[
        ],
        justification=[
            "This visual comes from the Chromoscope visualization database."
        ],
        caption="Integrative visualization of genomic alterations across the human genome. A circos plot (top) depicts structural variants, including translocations, duplications, deletions, and inversions, across chromosomes. Inner tracks indicate regions of copy number gain, loss of heterozygosity (LOH), and putative driver events. The expanded linear view (bottom) shows chromosome 1 in detail, with ideogram, annotated genes, point mutations stratified by substitution class, indels, and copy number variants. Together, these tracks highlight the co-occurrence of single-nucleotide variants, indels, and large-scale structural rearrangements in the context of chromosomal architecture.",
        taxonomy_type=QueryTaxonomy.BROWSE,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.MULTIVIEW,
    )

df = add_row(
        df,
        query_template="Browse the structural data.",
        spec=(
        
        {
  "layout": "linear",
  "arrangement": "vertical",
  "centerRadius": 0.5,
  "assembly": "hg19",
  "spacing": 40,
  "style": {
    "outlineWidth": 1,
    "outline": "lightgray",
    "enableSmoothPath": False
  },
  "views": [
    {
      "arrangement": "vertical",
      "views": [
        {
          "xOffset": 560,
          "static": True,
          "layout": "circular",
          "spacing": 1,
          "style": {
            "outlineWidth": 1,
            "outline": "lightgray"
          },
          "tracks": [
            {
              "name": "Ideogram",
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-top-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
                "type": "csv",
                "chromosomeField": "Chromosome",
                "genomicFields": [
                  "chromStart",
                  "chromEnd"
                ]
              },
              "tracks": [
                {
                  "mark": "rect"
                },
                {
                  "mark": "brush",
                  "x": {
                    "linkingId": "mid-scale"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "stroke": {
                    "value": "#0070DC"
                  },
                  "color": {
                    "value": "#AFD8FF"
                  },
                  "opacity": {
                    "value": 0.5
                  }
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 600,
              "height": 100
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-top-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/a25e1eaf-fbe6-4aba-8d39-c2b4e84464cf",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 10
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 600,
              "height": 40
            },
            {
              "id": "driver-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-top-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "gain-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-top-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 600,
              "height": 40
            },
            {
              "id": "loh-top-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rect",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-top-sv",
              "title": "",
              "alignment": "overlay",
              "experimental": {
                "mouseEvents": {
                  "click": True,
                  "mouseOver": True,
                  "groupMarksByField": "sv_id"
                },
                "performanceMode": True
              },
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 64
                  },
                  "ye": {
                    "value": 80
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 16
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 32
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 48
                  },
                  "ye": {
                    "value": 64
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                }
              ],
              "y": {
                "value": 16
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 600,
              "height": 80
            }
          ]
        },
        {
          "linkingId": "mid-scale",
          "xDomain": {
            "chromosome": "chr1"
          },
          "layout": "linear",
          "tracks": [
            {
              "title": "  Ideogram",
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-ideogram",
              "alignment": "overlay",
              "data": {
                "url": "https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG19.Human.CytoBandIdeogram.csv",
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
                "type": "genomic"
              },
              "xe": {
                "field": "chromEnd",
                "type": "genomic"
              },
              "strokeWidth": {
                "value": 0
              },
              "width": 1720,
              "height": 18
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-driver",
              "title": "  Putative Driver",
              "data": {
                "url": "blob:https://chromoscope.bio/22eb958a-a29e-43cf-8b30-766f41aebf8f",
                "type": "csv",
                "separator": "\t",
                "chromosomeField": "chr",
                "genomicFields": [
                  "pos"
                ]
              },
              "dataTransform": [
                {
                  "type": "replace",
                  "field": "biallelic",
                  "replace": [
                    {
                      "from": "yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "no",
                      "to": "· "
                    },
                    {
                      "from": "Yes",
                      "to": "⊙ "
                    },
                    {
                      "from": "No",
                      "to": "· "
                    }
                  ],
                  "newField": "prefix"
                },
                {
                  "type": "concat",
                  "fields": [
                    "prefix",
                    "gene"
                  ],
                  "newField": "geneWithPrefix",
                  "separator": ""
                }
              ],
              "mark": "text",
              "x": {
                "field": "pos",
                "type": "genomic"
              },
              "text": {
                "field": "geneWithPrefix",
                "type": "nominal"
              },
              "color": {
                "value": "black"
              },
              "row": {
                "field": "row",
                "type": "nominal"
              },
              "style": {
                "textFontWeight": "normal"
              },
              "size": {
                "value": 14
              },
              "tooltip": [
                {
                  "field": "pos",
                  "alt": "Position",
                  "type": "genomic"
                },
                {
                  "field": "ref",
                  "alt": "REF",
                  "type": "nominal"
                },
                {
                  "field": "alt",
                  "alt": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "category",
                  "alt": "Category",
                  "type": "nominal"
                },
                {
                  "field": "top_category",
                  "alt": "Top Category",
                  "type": "nominal"
                },
                {
                  "field": "biallelic",
                  "alt": "Biallelic",
                  "type": "nominal"
                },
                {
                  "field": "transcript_consequence",
                  "alt": "Transcript Consequence",
                  "type": "nominal"
                },
                {
                  "field": "protein_mutation",
                  "alt": "Protein Mutation",
                  "type": "nominal"
                },
                {
                  "field": "allele_fraction",
                  "alt": "Allele Fraction",
                  "type": "nominal"
                },
                {
                  "field": "mutation_type",
                  "alt": "Mutation Type",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 40
            },
            {
              "id": "driver-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-gene",
              "title": "  Gene Annotation",
              "template": "gene",
              "data": {
                "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation-hg19",
                "type": "beddb",
                "genomicFields": [
                  {
                    "index": 1,
                    "name": "start"
                  },
                  {
                    "index": 2,
                    "name": "end"
                  }
                ],
                "valueFields": [
                  {
                    "index": 5,
                    "name": "strand",
                    "type": "nominal"
                  },
                  {
                    "index": 3,
                    "name": "name",
                    "type": "nominal"
                  }
                ],
                "exonIntervalFields": [
                  {
                    "index": 12,
                    "name": "start"
                  },
                  {
                    "index": 13,
                    "name": "end"
                  }
                ]
              },
              "encoding": {
                "startPosition": {
                  "field": "start"
                },
                "endPosition": {
                  "field": "end"
                },
                "strandColor": {
                  "field": "strand",
                  "range": [
                    "gray"
                  ]
                },
                "strandRow": {
                  "field": "strand"
                },
                "opacity": {
                  "value": 0.4
                },
                "geneHeight": {
                  "value": 20
                },
                "geneLabel": {
                  "field": "name"
                },
                "geneLabelFontSize": {
                  "value": 20
                },
                "geneLabelColor": {
                  "field": "strand",
                  "range": [
                    "black"
                  ]
                },
                "geneLabelStroke": {
                  "value": "white"
                },
                "geneLabelStrokeThickness": {
                  "value": 4
                },
                "geneLabelOpacity": {
                  "value": 1
                },
                "type": {
                  "field": "type"
                }
              },
              "tooltip": [
                {
                  "field": "name",
                  "type": "nominal"
                },
                {
                  "field": "strand",
                  "type": "nominal"
                }
              ],
              "width": 1720,
              "height": 60
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-mutation",
              "title": "  Point Mutation",
              "style": {
                "background": "#FFFFFF",
                "inlineLegend": True
              },
              "data": {
                "type": "vcf",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.sorted.vcf.gz.tbi",
                "sampleLength": 500
              },
              "alignment": "overlay",
              "dataTransform": [
                {
                  "field": "DISTPREV",
                  "type": "filter",
                  "oneOf": [0],
                  "not": True
                }
              ],
              "tracks": [
                {
                  "dataTransform": [
                    {
                      "field": "DISTPREV",
                      "type": "filter",
                      "oneOf": [0],
                      "not": True
                    }
                  ]
                },
                {
                  "dataTransform": [
                    {
                      "field": "POS",
                      "type": "filter",
                      "oneOf": [null]
                    }
                  ],
                  "stroke": {
                    "field": "SUBTYPE",
                    "type": "nominal",
                    "legend": True,
                    "domain": [
                      "C\u003EA",
                      "C\u003EG",
                      "C\u003ET",
                      "T\u003EA",
                      "T\u003EC",
                      "T\u003EG"
                    ]
                  },
                  "strokeWidth": {
                    "value": 10
                  },
                  "opacity": {
                    "value": 0.3
                  }
                }
              ],
              "mark": "point",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "SUBTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "C\u003EA",
                  "C\u003EG",
                  "C\u003ET",
                  "T\u003EA",
                  "T\u003EC",
                  "T\u003EG"
                ]
              },
              "y": {
                "field": "DISTPREVLOGE",
                "type": "quantitative",
                "axis": "right",
                "range": [10, 50]
              },
              "opacity": {
                "value": 0.9
              },
              "tooltip": [
                {
                  "field": "DISTPREV",
                  "type": "nominal",
                  "format": "s1",
                  "alt": "Distance To Previous Mutation (BP)"
                },
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "SUBTYPE",
                  "type": "nominal"
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
              "width": 1720,
              "height": 60
            },
            {
              "id": "mutation-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                 },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-indel",
              "title": "  Indel",
              "style": {
                "background": "#F6F6F6",
                "inlineLegend": True
              },
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20161006.somatic.indel.sorted.vcf.gz",
                "indexUrl": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20161006.somatic.indel.sorted.vcf.gz.tbi",
                "type": "vcf",
                "sampleLength": 500
              },
              "dataTransform": [
                {
                  "type": "concat",
                  "fields": [
                    "REF",
                    "ALT"
                  ],
                  "separator": " → ",
                  "newField": "LAB"
                },
                {
                  "type": "replace",
                  "field": "MUTTYPE",
                  "replace": [
                    {
                      "from": "insertion",
                      "to": "Insertion"
                    },
                    {
                      "from": "deletion",
                      "to": "Deletion"
                    }
                  ],
                  "newField": "MUTTYPE"
                }
              ],
              "alignment": "overlay",
              "tracks": [
                {
                  "size": {
                    "value": 19
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "GT",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                },
                {
                  "xe": {
                    "field": "POSEND",
                    "type": "genomic",
                    "axis": "top"
                  },
                  "visibility": [
                    {
                      "target": "track",
                      "operation": "LTET",
                      "measure": "zoomLevel",
                      "threshold": 1000
                    }
                  ]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "POS",
                "type": "genomic"
              },
              "color": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "row": {
                "field": "MUTTYPE",
                "type": "nominal",
                "legend": False,
                "domain": [
                  "Insertion",
                  "Deletion"
                ]
              },
              "tooltip": [
                {
                  "field": "POS",
                  "type": "genomic"
                },
                {
                  "field": "POSEND",
                  "type": "genomic"
                },
                {
                  "field": "MUTTYPE",
                  "type": "nominal"
                },
                {
                  "field": "ALT",
                  "type": "nominal"
                },
                {
                  "field": "REF",
                  "type": "nominal"
                },
                {
                  "field": "QUAL",
                  "type": "quantitative"
                }
              ],
              "opacity": {
                "value": 0.9
              },
              "width": 1720,
              "height": 40
            },
            {
              "id": "indel-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-cnv",
              "title": "  Copy Number Variants",
              "style": {
                "background": "#FFFFFF"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "alignment": "overlay",
              "tracks": [
                {
                  "y": {
                    "field": "total_cn",
                    "type": "quantitative",
                    "axis": "right",
                    "grid": True,
                    "range": [10, 50]
                  },
                  "color": {
                    "value": "#808080"
                  }
                }
              ],
              "tooltip": [
                {
                  "field": "total_cn",
                  "type": "quantitative"
                },
                {
                  "field": "major_cn",
                  "type": "quantitative"
                },
                {
                  "field": "minor_cn",
                  "type": "quantitative"
                }
              ],
              "size": {
                "value": 5
              },
              "stroke": {
                "value": "#808080"
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "width": 1720,
              "height": 60
            },
            {
              "id": "cnv-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-gain",
              "title": "  Gain",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "total_cn",
                  "inRange": [5, 999]
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#5CB6EA"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "gain-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-loh",
              "title": "  Loss of Heterozygosity (LOH)",
              "style": {
                "background": "#F6F6F6"
              },
              "data": {
                "separator": "\t",
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.consensus.20170119.somatic.cna.txt",
                "type": "csv",
                "chromosomeField": "chromosome",
                "genomicFields": [
                  "start",
                  "end"
                ]
              },
              "dataTransform": [
                {
                  "type": "filter",
                  "field": "minor_cn",
                  "inRange": [0, 0.01]
                },
                {
                  "type": "filter",
                  "field": "total_cn",
                  "oneOf": [
                    "0"
                  ],
                  "not": True
                }
              ],
              "mark": "rect",
              "x": {
                "field": "start",
                "type": "genomic"
              },
              "xe": {
                "field": "end",
                "type": "genomic"
              },
              "color": {
                "value": "#D6641E"
              },
              "width": 1720,
              "height": 20
            },
            {
              "id": "loh-mid-boundary",
              "data": {
                "type": "json",
                "chromosomeField": "c",
                "genomicFields": [
                  "p"
                ],
                "values": [
                  {
                    "c": "chr2",
                    "p": 0
                  },
                  {
                    "c": "chr3",
                    "p": 0
                  },
                  {
                    "c": "chr4",
                    "p": 0
                  },
                  {
                    "c": "chr5",
                    "p": 0
                  },
                  {
                    "c": "chr6",
                    "p": 0
                  },
                  {
                    "c": "chr7",
                    "p": 0
                  },
                  {
                    "c": "chr8",
                    "p": 0
                  },
                  {
                    "c": "chr9",
                    "p": 0
                  },
                  {
                    "c": "chr10",
                    "p": 0
                  },
                  {
                    "c": "chr11",
                    "p": 0
                  },
                  {
                    "c": "chr12",
                    "p": 0
                  },
                  {
                    "c": "chr13",
                    "p": 0
                  },
                  {
                    "c": "chr14",
                    "p": 0
                  },
                  {
                    "c": "chr15",
                    "p": 0
                  },
                  {
                    "c": "chr16",
                    "p": 0
                  },
                  {
                    "c": "chr17",
                    "p": 0
                  },
                  {
                    "c": "chr18",
                    "p": 0
                  },
                  {
                    "c": "chr19",
                    "p": 0
                  },
                  {
                    "c": "chr20",
                    "p": 0
                  },
                  {
                    "c": "chr21",
                    "p": 0
                  },
                  {
                    "c": "chrX",
                    "p": 0
                  },
                  {
                    "c": "chrY",
                    "p": 0
                  }
                ]
              },
              "mark": "rule",
              "x": {
                "field": "p",
                "type": "genomic"
              },
              "color": {
                "value": "lightgray"
              },
              "opacity": {
                "value": 0.5
              },
              "overlayOnPreviousTrack": True
            },
            {
              "id": "fa718a69-7d09-424b-90a3-4839ba7dc9b2-mid-sv",
              "title": "  Structural Variants",
              "alignment": "overlay",
              "experimental": {
                "mouseEvents": {
                  "click": True,
                  "mouseOver": True,
                  "groupMarksByField": "sv_id"
                },
                "performanceMode": True
              },
              "data": {
                "url": "https://somatic-browser-test.s3.amazonaws.com/PCAWG/Myeloid-AML/fa718a69-7d09-424b-90a3-4839ba7dc9b2.pcawg_consensus_1.6.161116.somatic.sv.bedpe",
                "type": "csv",
                "separator": "\t",
                "genomicFieldsToConvert": [
                  {
                    "chromosomeField": "chrom1",
                    "genomicFields": [
                      "start1",
                      "end1"
                    ]
                  },
                  {
                    "chromosomeField": "chrom2",
                    "genomicFields": [
                      "start2",
                      "end2"
                    ]
                  }
                ]
              },
              "mark": "withinLink",
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": True
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Translocation"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 200
                  },
                  "ye": {
                    "value": 250
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  },
                  "stroke": {
                    "value": "grey"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Duplication"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Deletion"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 50
                  },
                  "ye": {
                    "value": 1
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (TtT)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 100
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ],
                      "not": False
                    },
                    {
                      "type": "filter",
                      "field": "svclass",
                      "oneOf": [
                        "Inversion (HtH)"
                      ],
                      "not": False
                    }
                  ],
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "xe": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "y": {
                    "value": 150
                  },
                  "ye": {
                    "value": 200
                  },
                  "flipY": True,
                  "opacity": {
                    "value": 1
                  },
                  "strokeWidth": {
                    "value": 2
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand1",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "+"
                      ]
                    }
                  ],
                  "mark": "triangleLeft",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "right"
                  }
                },
                {
                  "dataTransform": [
                    {
                      "type": "filter",
                      "field": "strand2",
                      "oneOf": [
                        "-"
                      ]
                    }
                  ],
                  "mark": "triangleRight",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "size": {
                    "value": 5
                  },
                  "y": {
                    "value": 250
                  },
                  "stroke": {
                    "value": 0
                  },
                  "style": {
                    "align": "left"
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "start1",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                },
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
                        {
                          "from": "DUP",
                          "to": "Duplication"
                        },
                        {
                          "from": "TRA",
                          "to": "Translocation"
                        },
                        {
                          "from": "DEL",
                          "to": "Deletion"
                        },
                        {
                          "from": "t2tINV",
                          "to": "Inversion (TtT)"
                        },
                        {
                          "from": "h2hINV",
                          "to": "Inversion (HtH)"
                        }
                      ],
                      "newField": "svclass"
                    },
                    {
                      "type": "filter",
                      "field": "sv_id",
                      "oneOf": [
                        ""
                      ]
                    }
                  ],
                  "mark": "rule",
                  "x": {
                    "field": "end2",
                    "type": "genomic"
                  },
                  "color": {
                    "value": "black"
                  },
                  "strokeWidth": {
                    "value": 1
                  },
                  "opacity": {
                    "value": 1
                  },
                  "style": {
                    "dashed": [3, 3]
                  }
                }
              ],
              "y": {
                "value": 50
              },
              "color": {
                "field": "svclass",
                "type": "nominal",
                "legend": True,
                "domain": [
                  "Gain",
                  "LOH",
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "#5CB6EA",
                  "#D6641E",
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "stroke": {
                "field": "svclass",
                "type": "nominal",
                "domain": [
                  "Translocation",
                  "Duplication",
                  "Deletion",
                  "Inversion (TtT)",
                  "Inversion (HtH)"
                ],
                "range": [
                  "lightgrey",
                  "#409F7A",
                  "#3275B4",
                  "#CC7DAA",
                  "#E6A01B"
                ]
              },
              "strokeWidth": {
                "value": 1
              },
              "opacity": {
                "value": 0.7
              },
              "tooltip": [
                {
                  "field": "start1",
                  "type": "genomic"
                },
                {
                  "field": "end2",
                  "type": "genomic"
                },
                {
                  "field": "strand1",
                  "type": "nominal"
                },
                {
                  "field": "strand2",
                  "type": "nominal"
                },
                {
                  "field": "svclass",
                  "type": "nominal"
                },
                {
                  "field": "sv_id",
                  "type": "nominal"
                },
                {
                  "field": "pe_support",
                  "type": "nominal"
                }
              ],
              "style": {
                "linkStyle": "elliptical",
                "linkMinHeight": 0.7,
                "mouseOver": {
                  "stroke": "#242424",
                  "strokeWidth": 1
                },
                "withinLinkVerticalLines": True
              },
              "width": 1720,
              "height": 250
            }
          ]
        }
      ]
    }
  ]
}




            
            
        ),
        constraints=[
        ],
        justification=[
            "This visual comes from the Chromoscope visualization database."
        ],
        caption="Integrative visualization of genomic alterations across the human genome. A circos plot (top) depicts structural variants, including translocations, duplications, deletions, and inversions, across chromosomes. Inner tracks indicate regions of copy number gain, loss of heterozygosity (LOH), and putative driver events. The expanded linear view (bottom) shows chromosome 1 in detail, with ideogram, annotated genes, point mutations stratified by substitution class, indels, and copy number variants. Together, these tracks highlight the co-occurrence of single-nucleotide variants, indels, and large-scale structural rearrangements in the context of chromosomal architecture.",
        taxonomy_type=QueryTaxonomy.BROWSE,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.MULTIVIEW,
    )
