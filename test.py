########################################################################################################################
#
# test.py
#   - Program to test the functionality of the API for various events
#   - This program is not a part of the API and should be run locally (AWS connection details may be needed)
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
########################################################################################################################
import json
import os
import logging
from datetime import datetime

os.environ['region_name'] = 'us-east-1'
os.environ['athena_database'] = 'macompanies-test'
os.environ['s3_bucket_name'] = 'sysco-macompanies-test'
os.environ['athena_output_folder'] = 'AthenaOutput'

from index import lambda_handler
from source.config import config as cfg

logging.basicConfig(filename="test.log", format='%(asctime)s %(message)s')
logger = cfg.logger
export_date_obj = datetime.now()

like_search_event = {
    "httpMethod": "POST",
    "path": '/search_recruiting_data',
    "body": {
        "table": "applicant_info_2",
        "search": {
            "approver_user_sys_id": ["sf"]
        }
    }
}
like_search_event['body'] = json.dumps(like_search_event['body'])

exact_search_event = {
    "httpMethod": "POST",
    "path": '/mna/search_greco_data',
    "body": {
        "table": "greco_3rd_party_sick_pay_report",
        "sort": {
            "id": "Ascending"
        }
    }
}
exact_search_event['body'] = json.dumps(exact_search_event['body'])

date_range_search_event = {
    "httpMethod": "POST",
    "path": '/search_recruiting_data',
    "body": {
        "table": "applications",
        "search": {
            "application_date": ["1/20/2017"]
        }
    }
}
date_range_search_event['body'] = json.dumps(date_range_search_event['body'])

# logger = config.logger
# logger.debug('yash')

test_response = lambda_handler(exact_search_event, '_')
with open("response.json", 'w') as f:
    f.write(json.dumps(json.loads(test_response["body"]), indent=4))

print(test_response)
