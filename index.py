########################################################################################################################
#
# index.py
#   - Main script that contains the lambda handler function for the API
#   - Redirects the code flow to respective function according to the API path
#
# Author(s): yash parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
########################################################################################################################
from source.code_files.search_greco_data import search_greco_data
from source.code_files.export_greco_file import export_greco_file
from source.config import config as cfg

import json
import time


logger = cfg.logger

# Lambda handler function that will be called whenever the API is triggered
def lambda_handler(event, _):
    lambda_exec_start_time = time.time()
    logger.info(f'Event received:\n{event}')
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    logger.info(f'httpMethod: {http_method}\npath: {path}')

    if http_method == 'POST' and path == '/mna/search_greco_data':
        query_sting_params = event.get('queryStringParameters', {})
        if query_sting_params != {}:
            page_no = int(query_sting_params['page'])
            page_size = int(query_sting_params['pagesize'])
            logger.info(f'page_no: {page_no}\npage_size: {page_size}')
        else:
            logger.warn(f'queryStringParameters is empty; setting default page_no and page_size values')
            page_no = 1
            page_size = 20
            logger.info(f'page_no: {page_no}\npage_size: {page_size}')
        body = json.loads(event.get('body', ''))
        logger.info(f'body: {body}')
        logger.info(f"Invoking 'search_greco_data' function")
        status, response = search_greco_data(body, page_no, page_size)
    elif http_method == 'POST' and path == '/mna/export_greco_file':
        body = json.loads(event.get('body', ''))
        logger.info(f'body: {body}')
        logger.info(f"Invoking 'export_greco_file' function")
        status, response = export_greco_file(body)
    else:
        logger.info(f"Reached 'Invalid Request' section")
        status = 500
        response = {
            'message': 'Invalid Request'
        }

    response_body = '{"status":' + str(status) + \
                    ',"result":' + json.dumps(response) + '}'

    final_response = {
        'statusCode': status,
        'body': response_body,
        'headers':
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE',
                'Access-Control-Allow-Headers': 'X-Requested-With,content-type'
            }
    }
    lambda_exec_duration = '{0:.2f}s'.format(time.time() - lambda_exec_start_time)
    logger.info(f"Lambda execution duration: {lambda_exec_duration}")
    return final_response
