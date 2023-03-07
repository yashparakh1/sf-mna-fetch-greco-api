########################################################################################################################
#
# export_greco_file.py
#   - Program for file export functionality
#   - Returns the pre-signed URL of the result file on successful query execution
#   - Query execution ID is the file identifier in AWS S3 where the Athena output is stored
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-22 - ypar3236 - Created
#
########################################################################################################################
from source.code_files.aws_utils import execute_query, check_execution, generate_pre_signed_url, build_query
from source.config import config as cfg
import boto3
import time

logger = cfg.logger


# Main function of this program
def export_greco_file(body):
    export_function_start_time = time.time()
    athena_client = boto3.client("athena", region_name=cfg.region_name)
    logger.info("athena_client created successfully")
    s3_client = boto3.client("s3", region_name=cfg.region_name)
    logger.info("s3_client created successfully")

    try:
        count_query, select_query = build_query(body, -1, -1)

        select_query_response = execute_query(athena_client, select_query)
        execution_id = select_query_response["QueryExecutionId"]
        state = check_execution(athena_client, execution_id)
        if state in ['FAILED', 'TIMEOUT']:
            logger.error(f'Execution failed for count: status: {state}')
            raise Exception(f"Execution failed for select query; state={state}")
        else:
            status = 200
            pre_signed_url = generate_pre_signed_url(s3_client, execution_id)
            response = {
                'pre-signed URL': pre_signed_url
            }
    except Exception as e:
        status = 500
        response = {
            'error_message': str(e)
        }

    export_function_duration = '{0:.2f}s'.format(time.time() - export_function_start_time)
    logger.info(f'Export function execution completed; Status: {status}; Time taken: {export_function_duration}')
    return status, response
