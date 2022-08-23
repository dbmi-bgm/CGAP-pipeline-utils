#################################################################
#   Libraries
#################################################################
import sys, os
import pytest
import glob
from pipeline_utils.lib import yaml_parser

#################################################################
#   Tests
#################################################################
def test_metaworkflow():
    """
    """
    res = [
        {
          "aliases": ["cgap-core:gatk-HC-GT-pipeline_v1.0.0"],
          "description": "Pipeline to run gatk-HC and gatk-GT to call and genotype variants",
          "input": [
            {
              "argument_name": "input_vcf",
              "argument_type": "file",
              "dimensionality": 1
            },
            {
              "argument_name": "reference",
              "argument_type": "file",
              "files": [{"dimension": "0", "file": "cgap-core:reference_genome_hg38"}]
            },
            {
              "argument_name": "samples",
              "argument_type": "parameter",
              "value": ["SAMPLENAME"],
              "value_type": "json"
            }
          ],
          "institution": "/institutions/hms-dbmi/",
          "name": "gatk-HC-GT-pipeline",
          "project": "/projects/cgap-core/",
          "title": "gatk-HC and gatk-GT pipeline, v1.0.0",
          "version": "v1.0.0",
          "workflows": [
            {
              "config": {
                "ebs_size": "2x",
                "ec2_type": "m.5xlarge"
              },
              "custom_pf_fields": {
                "HC_vcf": {
                  "description": "output from gatk-HC",
                  "file_type": "hc-vcf",
                  "linkto_location": [
                    "SampleProcessing"
                  ]
                }
              },
              "input": [
                {
                  "argument_name": "vcf",
                  "argument_type": "file",
                  "extra_dimension": 1,
                  "mount": True,
                  "source_argument_name": "input_vcf",
                  "unzip": "gz"
                },
                {
                  "argument_name": "reference_genome",
                  "argument_type": "file",
                  "source_argument_name": "reference"
                },
                {
                  "argument_name": "nthreads",
                  "argument_type": "parameter",
                  "value": 16,
                  "value_type": "integer"
                }
              ],
              "name": "gatk-HC",
              "workflow": "cgap-core:gatk-HC_v1.0.0"
            },
            {
              "config": {
                "ebs_size": "3x",
                "ec2_type": "c.5xlarge"
              },
              "custom_pf_fields": {
                "GT_vcf": {
                  "description": "output from gatk-GT",
                  "file_type": "GT-vcf",
                  "higlass_file": True,
                  "variant_type": "SNV"
                }
              },
              "input": [
                {
                  "argument_name": "input_vcf_HC",
                  "argument_type": "file",
                  "gather": 0,
                  "scatter": 0,
                  "source": "gatk-HC",
                  "source_argument_name": "HC_vcf"
                },
                {
                  "argument_name": "sample_name",
                  "argument_type": "parameter",
                  "input_dimension": 1,
                  "source_argument_name": "samples",
                  "value_type": "json"
                }
              ],
              "name": "gatk-GT",
              "workflow": "cgap-core:gatk-GT_v1.0.0"
            }
          ]
        },
        {
          "accession": "GAPFIXRDPDK1",
          "aliases": ["cgap-core:gatk-HC-pipeline_v1.0.0"],
          "description": "Pipeline to run gatk-HC to call variants",
          "input": [
            {
              "argument_name": "input_vcf",
              "argument_type": "file"
            },
            {
              "argument_name": "reference",
              "argument_type": "file",
              "files": [{"dimension": "0", "file": "cgap-core:reference_genome_hg38"},
                        {"dimension": "1", "file": "cgap-core:reference_bam_hg38"}]
            },
            {
              "argument_name": "samples",
              "argument_type": "parameter",
              "value_type": "json"
            }
          ],
          "institution": "/institutions/hms-dbmi/",
          "name": "gatk-HC-pipeline",
          "project": "/projects/cgap-core/",
          "title": "gatk-HC-pipeline, v1.0.0",
          "uuid": "1936f246-22e1-45dc-bb5c-9cfd55537fe9",
          "version": "v1.0.0",
          "workflows": [
            {
              "config": {
                "ebs_size": "2x",
                "ec2_type": "m.5xlarge"
              },
              "custom_pf_fields": {
                "HC_vcf": {
                  "file_type": "hc-vcf"
                }
              },
              "input": [
                {
                  "argument_name": "vcf",
                  "argument_type": "file",
                  "source_argument_name": "input_vcf"
                },
                {
                  "argument_name": "reference",
                  "argument_type": "file"
                },
                {
                  "argument_name": "samples",
                  "argument_type": "parameter",
                  "value_type": "json"
                }
              ],
              "name": "gatk-HC",
              "workflow": "cgap-core:gatk-HC_v1.0.0"
            }
          ]
        }
    ]

    for i, fn in enumerate(glob.glob('tests/repo_correct/portal_objects/metaworkflows/*.yaml')):
        for d in yaml_parser.load_yaml(fn):
            d_ = yaml_parser.YAMLMetaWorkflow(d).to_json(
                                INSTITUTION='hms-dbmi',
                                PROJECT='cgap-core',
                                VERSION='v1.0.0'
                            )
            # check
            assert d_ == res[i]