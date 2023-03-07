########################################################################################################################
#
# aws_utils.py
#   - Utility script containing helper functions to perform operations on AWS Services
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
# Known Limitations:
#   * On query execution, AWS Athena doesn't provide a callback to notify the completion. We need to manually check for
#     the execution status
#
########################################################################################################################
from source.config import config as cfg
from botocore.exceptions import ClientError
import time
from source.config.column_config import column_dict

logger = cfg.logger


# Function to perform query execution on AWS Athena
def execute_query(athena_client, query):
    logger.info(f"Initializing query execution for the query:\n{query}")
    initialization_start_time = time.time()
    query_response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": cfg.athena_database},
        ResultConfiguration={
            "OutputLocation": cfg.s3_output_location_uri,
        }
    )
    initialization_duration = '{0:.2f}s'.format(time.time() - initialization_start_time)
    logger.info(f"Initialized query execution; Time taken: {initialization_duration}")

    return query_response


# Function to monitor the execution of the query performed on AWS Athena
def check_execution(athena_client, execution_id):
    logger.info('Checking query execution')
    for i in range(1, 61):
        try:
            query_execution = athena_client.get_query_execution(
                QueryExecutionId=execution_id
            )
            state = query_execution['QueryExecution']['Status']['State']
            logger.info(f"attempt-{i}: state = {state}")
            if state in ['RUNNING', 'QUEUED']:
                time.sleep(1)
                continue
            else:
                if state == 'FAILED':
                    logger.error(f"{query_execution['QueryExecution']['Status']['StateChangeReason']}")
                return state
        except Exception as e:
            logger.error(f"error while checking execution: {str(e)}")
            return 'FAILED'
    return 'TIMEOUT'


# Function to fetch the result set from AWS Athena
def get_results(athena_client, execution_id):
    logger.info('Getting results')
    fetch_results_start_time = time.time()
    try:
        query_results = athena_client.get_query_results(
            QueryExecutionId=execution_id
        )
        result_set = query_results['ResultSet']
        fetch_results_duration = '{0:.2f}s'.format(time.time() - fetch_results_start_time)
        logger.info(f"Fetched results successfully; Time taken: {fetch_results_duration}")
        return result_set
    except Exception as e:
        logger.error(f"Error while fetching results: {str(e)}")
        raise e


# Function to generate pre-signed URL to download the result file in AWS S3
def generate_pre_signed_url(s3_client, execution_id):
    logger.info("Generating pre-signed URL")
    s3_output_file_path = f'{cfg.athena_output_folder}/{execution_id}.csv'  # key
    logger.info(f"File path: {s3_output_file_path}")
    generate_pre_signed_url_start_time = time.time()
    try:
        pre_signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': cfg.s3_bucket_name,
                'Key': s3_output_file_path
            },
            ExpiresIn=604800  # 7 days expiry duration
        )
    except ClientError as e:
        logger.error(f"Error while generating pre-signed URL: {str(e)}")
        return None
    generate_pre_signed_url_duration = '{0:.2f}s'.format(time.time() - generate_pre_signed_url_start_time)
    logger.info(f"Generated pre-signed URL successfully; Time taken: {generate_pre_signed_url_duration}")
    return pre_signed_url


# Function to build query as per request body
def build_query(body, page_no, page_size):
    logger.info("Building the query")
    query_build_start_time = time.time()

    table = body['table']
    search_data = body.get('search', '')
    sort_data = body.get('sort', '')

    cols = ['"' + col + '"' for col in column_dict[table]["columns"]]
    col_string = ','.join(cols)
    select_query = f"SELECT * FROM {table}"

    logger.info("select_query initialized")

    if search_data != '':
        logger.info("Building 'WHERE' clause")
        search_where_clause = ''
        keyword = 'WHERE'
        for key in search_data:
            column = key
            value = search_data[key][0]

            if table in column_dict.keys():
                if 'timestamp' in column_dict[table].keys() and column in column_dict[table]['timestamp']:
                    logger.info(f"Timestamp column: {column}")
                    query = f" {keyword} SUBSTRING({column}, 1, {len(value)}) = '{value}'"
                elif 'date_range' in column_dict[table].keys() and column in column_dict[table]['date_range'] and len(
                        search_data[key]) == 2:
                    logger.info(f"Date-Range column: {column}")
                    value_2 = search_data[key][1]
                    query = f" {keyword} date_parse({column}, '%m/%d/%Y') BETWEEN CAST(date_parse('{value}', '%m/%d/%Y') AS date) AND CAST(date_parse('{value_2}', '%m/%d/%Y') AS date)"
                elif 'exact_match' in column_dict[table].keys() and column in column_dict[table]['exact_match']:
                    logger.info(f"Exact-Match column: {column}")
                    query = f" {keyword} {column} = '{value}'"
                else:
                    logger.info(f"Like-Match column: {column}")
                    value = f'%{value.upper()}%'
                    query = f" {keyword} UPPER({column}) LIKE '{value}'"
            else:
                logger.info(f"Like-Match column: {column}")
                value = f'%{value.upper()}%'
                query = f" {keyword} UPPER({column}) LIKE '{value}'"
            keyword = 'AND'
            search_where_clause += query
        select_query += search_where_clause
        logger.info("'WHERE' clause built")

    count_query = select_query.replace('*', 'COUNT(*)', 1)
    select_query = select_query.replace('*', col_string)

    logger.info(logger.info(f"Count query built: {count_query}"))

    if sort_data != '':
        logger.info("Building 'ORDER BY' clause")
        order_by_clause = " ORDER BY"
        for key in sort_data:
            column = key
            order = 'ASC' if sort_data[column] == 'Ascending' else 'DESC'
            logger.info(f"Column: {column}; Order: {order}")
            if key in column_dict[table]['ints']:
                query = f" CAST(\"{column}\" as int) {order}"
            else:
                query = f" LOWER({column}) {order}"
            order_by_clause += query
        select_query += order_by_clause
        logger.info("'ORDER BY' clause built")

    if page_no != -1:
        logger.info("Building 'PAGING' clause")
        offset = (page_no - 1) * page_size
        page_clause = f" OFFSET {offset} ROWS LIMIT {page_size}"
        select_query += page_clause
        logger.info("'PAGING' clause built")

    query_build_duration = '{0:.2f}s'.format(time.time() - query_build_start_time)
    logger.info(f"Select query built: {select_query}")
    logger.info(f"Time taken: {query_build_duration}")

    return count_query, select_query
