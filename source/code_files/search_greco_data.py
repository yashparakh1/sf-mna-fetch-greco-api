########################################################################################################################
#
# search_greco_data.py
#   - Program to fetch the required data in AWS Athena
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
########################################################################################################################
from source.code_files.aws_utils import execute_query, check_execution, get_results, build_query
from source.config import config as cfg

import boto3
import json
import pandas as pd
import time

logger = cfg.logger


# Function to transform the query result into the required structure
def reformat_response(data):
    logger.info("Reformatting the response.json from AWS Athena")
    reformat_start_time = time.time()
    cols = data['Rows'][0]['Data']
    columns = [c["VarCharValue"] for c in cols]

    row_objects = data['Rows'][1:]
    rows = []
    for obj in row_objects:
        row_data = obj['Data']
        row = [r["VarCharValue"] for r in row_data]
        rows.append(tuple(row))

    df = pd.DataFrame(rows, columns=columns)
    length = df.shape[0]

    response = [json.loads(df.iloc[index, :].to_json()) for index in range(length)]

    reformat_duration = '{0:.2f}s'.format(time.time() - reformat_start_time)
    logger.info(f'Reformatted response.json successfully; Time taken: {reformat_duration}')
    return response


# Main function of this program
def search_greco_data(body, page_no, page_size):
    search_function_start_time = time.time()
    athena_client = boto3.client(
        "athena",
        region_name=cfg.region_name
    )
    logger.info("athena_client created successfully")

    try:
        count_query, select_query = build_query(body, page_no, page_size)
        count_query_response = execute_query(athena_client, count_query)
        execution_id = count_query_response["QueryExecutionId"]
        state = check_execution(athena_client, execution_id)
        if state in ['FAILED', 'TIMEOUT']:
            logger.error(f'Execution failed for count: status: {state}')
            raise Exception(f"Execution failed for count query; state={state}")
        else:
            count_result_set = get_results(athena_client, execution_id)
            count = count_result_set['Rows'][1]["Data"][0]['VarCharValue']
            logger.info(f'count={count}')

        select_query_response = execute_query(athena_client, select_query)
        execution_id = select_query_response["QueryExecutionId"]
        state = check_execution(athena_client, execution_id)
        if state in ['FAILED', 'TIMEOUT']:
            logger.error(f'Execution failed for count: status: {state}')
            raise Exception(f"Execution failed for select query; state={state}")
        else:
            select_result_set = get_results(athena_client, execution_id)
            response_data = reformat_response(select_result_set)
            status = 200
            response = {
                'count': count,
                'data': response_data
            }

    except Exception as e:
        status = 500
        response = {
            'error_message': str(e)
        }

    search_function_duration = '{0:.2f}s'.format(time.time() - search_function_start_time)
    logger.info(f'Search function execution completed; Status: {status}; Time taken: {search_function_duration}')
    return status, response
