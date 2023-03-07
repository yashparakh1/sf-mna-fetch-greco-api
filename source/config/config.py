########################################################################################################################
#
# config.py - Python script for configuring the program
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
########################################################################################################################
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

region_name = os.environ['region_name']
athena_database = os.environ['athena_database']
s3_bucket_name = os.environ['s3_bucket_name']
athena_output_folder = os.environ['athena_output_folder']

s3_output_location_uri = f's3://{s3_bucket_name}/{athena_output_folder}/'