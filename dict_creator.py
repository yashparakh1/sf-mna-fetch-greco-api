######################################################################################################################
#
# dict_creator.py -
#   Utility script containing the code for generating the table meta-data used by the column_dict in
#   config.column_config
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
#
#######################################################################################################################

import os
os.environ['region_name'] = 'us-east-1'
os.environ['athena_database'] = 'macompanies-test'
os.environ['s3_bucket_name'] = 'sysco-macompanies-test'
os.environ['athena_output_folder'] = 'AthenaOutput'

import boto3
from source.code_files.aws_utils import execute_query, check_execution, get_results
import source.config.config as cfg
import json

athena_client = boto3.client("athena", region_name=cfg.region_name)

select_query_response = execute_query(athena_client, "show tables")
execution_id = select_query_response["QueryExecutionId"]
state = check_execution(athena_client, execution_id)
if state in ['FAILED', 'TIMEOUT']:
    raise Exception(f"Execution failed for select query; state={state}")
else:
    select_result_set = get_results(athena_client, execution_id)
    all_tables : list[str] = [list(x['Data'][0].values())[0] for x in select_result_set['Rows']]
    greco_tables : list[str] = []
    for x in all_tables:
        if x.startswith("greco"):
            greco_tables.append(x)
    print(greco_tables)

    with open("table_meta_data.json") as f:
        column_dict:dict = json.loads(f.read())

    for table in greco_tables:
        if table in column_dict:
            continue
        data_query_response = execute_query(athena_client, f"select * from \"{table}\"")
        execution_id = data_query_response["QueryExecutionId"]
        state = check_execution(athena_client, execution_id)
        if state in ['FAILED', 'TIMEOUT']:
            raise Exception(f"Execution failed for select query; state={state}")

        data_result = get_results(athena_client, execution_id)
        data_filtered = [[list(col.values())[0] for col in row['Data'][1:]] for row in data_result['Rows']]

        column_list: list[str] = data_filtered[0]
        data = data_filtered[1:]

        data_transformed = {column_list[i]: [r[i] for r in data] for i in range(len(column_list))}
        # print(data_transformed)

        column_dict[table] = {
            "columns": column_list,
            "exact_match": [],
            "timestamp": [],
            "date_range": [],
            "ints": []
        }

        for col in column_list:
            if col.__contains__("date"):
                column_dict[table]['timestamp'].append(col)
            is_col_int = True
            for val in data_transformed[col]:
                try:
                    v = int(val)
                except:
                    is_col_int = False
                    break
            if is_col_int:
                column_dict[table]['ints'].append(col)
                column_dict[table]['exact_match'].append(col)

        print(column_dict)
        # for col in all_columns:
        #     if col.__contains__('date'):
        #         column_dict[x]['timestamp'].append(col)

        # for col in all_columns:
        #     int_query_response = execute_query(athena_client, f"SELECT * FROM {x} WHERE cast(\"{col}\" as int) = 0")
        #     execution_id = int_query_response["QueryExecutionId"]
        #     state = check_execution(athena_client, execution_id)
        #     if state not in ['FAILED', 'TIMEOUT']:
        #         column_dict[x]['exact_match'].append(col)
        #         column_dict[x]['ints'].append(col)
        #     print(column_dict, end="\n\n")
        # print(column_dict, end="\n\n")

    with open("table_meta_data.json", 'w') as f:
        f.write(json.dumps(column_dict, indent=4))



