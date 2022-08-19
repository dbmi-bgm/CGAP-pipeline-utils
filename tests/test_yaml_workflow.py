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
def test_workflow():
    """
    """
    res = [
            {
                "aliases": ["cgap-core:gatk-HaplotypeCaller_v1.0.0"],
                "app_name": "gatk-HaplotypeCaller",
                "app_version": "v1.0.0",
                "arguments": [
                    {
                      "argument_type": "Input file",
                      "workflow_argument_name": "input_bam"
                    },
                    {
                      "argument_type": "parameter",
                      "workflow_argument_name": "nthreads"
                    },
                    {
                      "argument_format": "vcf_gz",
                      "argument_type": "Output processed file",
                      "secondary_file_formats": [
                        "vcf_gz_tbi"
                      ],
                      "workflow_argument_name": "output_vcf"
                    },
                    {
                      "argument_to_be_attached_to": "output_vcf",
                      "argument_type": "Output QC file",
                      "qc_html": False,
                      "qc_json": True,
                      "qc_table": False,
                      "qc_type": "quality_metric_vcfcheck",
                      "qc_zipped": False,
                      "workflow_argument_name": "vcfcheck"
                    }
                ],
                "description": "Run HaplotypeCaller from gatk package",
                "institution": "/institutions/hms-dbmi/",
                "name": "gatk-HaplotypeCaller_v1.0.0",
                "project": "/projects/cgap-core/",
                "software": [
                    "gatk_4.2.1",
                    "vcf-tools_5A63Aa1"
                ],
                "title": "HaplotypeCaller plus integity-check, v1.0.0",
                "wdl_child_filenames": [
                    "gatk-HaplotypeCaller.wdl",
                    "integrity-check.wdl"
                ],
                "wdl_directory_url": "s3://BUCKETCWL/test_pipeline/v1.0.0",
                "wdl_main_filename": "workflow_gatk-HaplotypeCaller-check.wdl",
                "workflow_language": "wdl"
            },
            {
                "accession": "GAPFIXRDPDK1",
                "aliases": ["cgap-core:gatk-HaplotypeCaller_v1.0.0"],
                "app_name": "gatk-HaplotypeCaller",
                "app_version": "v1.0.0",
                "arguments": [
                    {
                      "argument_type": "Input file",
                      "workflow_argument_name": "input_bam"
                    },
                    {
                      "argument_format": "vcf",
                      "argument_type": "Output processed file",
                      "secondary_file_formats": [],
                      "workflow_argument_name": "output_vcf"
                    }
                ],
                "description": "Run HaplotypeCaller from gatk package",
                "institution": "/institutions/hms-dbmi/",
                "name": "gatk-HaplotypeCaller_v1.0.0",
                "project": "/projects/cgap-core/",
                "software": [],
                "title": "gatk-HaplotypeCaller, v1.0.0",
                "cwl_child_filenames": [],
                "cwl_directory_url_v1": "s3://BUCKETCWL/test_pipeline/v1.0.0",
                "cwl_main_filename": "gatk-HaplotypeCaller-check.cwl",
                "uuid": "1936f246-22e1-45dc-bb5c-9cfd55537fe9"
            }
        ]

    for i, fn in enumerate(glob.glob('tests/repo_correct/portal_objects/workflows/*.yaml')):
        for d in yaml_parser.load_yaml(fn):
            d_ = yaml_parser.YAMLWorkflow(d).to_json(
                                INSTITUTION='hms-dbmi',
                                PROJECT='cgap-core',
                                VERSION='v1.0.0',
                                WFLBUCKET_URL='s3://BUCKETCWL/test_pipeline/v1.0.0'
                            )
            # check
            assert d_ == res[i]
