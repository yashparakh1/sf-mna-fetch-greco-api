########################################################################################################################
#
# column_config.py
#   - Contains a dictionary that maintains a list of columns for each greco table for which, exact-match,
#     date-range & timestamp search should be implemented
#
# Author(s): Yash Parakh
#
# Changelog:
#   2023-02-23 - ypar3236 - Created
#
########################################################################################################################

# Dictionary Structure:
# column_dict = {
#     "table_name": {
#        "columns": [List of all columns except seq_no]
#        "exact_match": [list of columns],
#        "timestamp": [list of columns],
#        "date_range": [list of columns]
#        "ints": [list of columns]
#     }
# }

column_dict = {
    "greco_3rd_party_sick_pay_report": {
        "columns": [
            "employee",
            "id",
            "location",
            "check_date",
            "earnings",
            "nt_earnings",
            "lt_earnings",
            "social_sec",
            "medicare",
            "other_taxes",
            "net"
        ],
        "exact_match": [
            "id",
            "location",
            "lt_earnings"
        ],
        "timestamp": [
            "check_date"
        ],
        "date_range": [],
        "ints": [
            "id",
            "location",
            "lt_earnings"
        ]
    },
    "greco_401k_census": {
        "columns": [
            "co",
            "id",
            "last_name",
            "first_name",
            "m",
            "ssn",
            "sex",
            "birthdate",
            "hiredate",
            "rehiredate",
            "termdate",
            "marital_status",
            "address_1",
            "address_2",
            "city",
            "state",
            "zip",
            "emp_status",
            "union_code",
            "er_pre",
            "er_post",
            "ee_pre",
            "ee_post",
            "loan_1",
            "loan_2",
            "loan_3",
            "loan_4",
            "loan_5",
            "loan_6",
            "loan_7",
            "loan_8",
            "loan_9",
            "hours",
            "gross",
            "ytd_er_pre",
            "ytd_er_post",
            "ytd_ee_pre",
            "ytd_ee_post",
            "ytd_loan_1",
            "ytd_loan_2",
            "ytd_load_3",
            "ytd_loan_4",
            "ytd_loan_5",
            "ytd_loan_6",
            "ytd_loan_7",
            "ytd_loan_8",
            "ytd_loan_9",
            "ytd_hours",
            "ytd_gross"
        ],
        "exact_match": [
            "co",
            "id",
            "last_name",
            "first_name",
            "m",
            "ssn",
            "sex",
            "birthdate",
            "hiredate",
            "rehiredate",
            "termdate",
            "marital_status",
            "address_1",
            "address_2",
            "city",
            "state",
            "zip",
            "emp_status",
            "union_code",
            "er_pre",
            "er_post",
            "ee_pre",
            "ee_post",
            "loan_1",
            "loan_2",
            "loan_3",
            "loan_4",
            "loan_5",
            "loan_6",
            "loan_7",
            "loan_8",
            "loan_9",
            "hours",
            "gross",
            "ytd_er_pre",
            "ytd_er_post",
            "ytd_ee_pre",
            "ytd_ee_post",
            "ytd_loan_1",
            "ytd_loan_2",
            "ytd_load_3",
            "ytd_loan_4",
            "ytd_loan_5",
            "ytd_loan_6",
            "ytd_loan_7",
            "ytd_loan_8",
            "ytd_loan_9",
            "ytd_hours",
            "ytd_gross"
        ],
        "timestamp": [
            "birthdate",
            "hiredate",
            "rehiredate",
            "termdate"
        ],
        "date_range": [],
        "ints": [
            "co",
            "id",
            "last_name",
            "first_name",
            "m",
            "ssn",
            "sex",
            "birthdate",
            "hiredate",
            "rehiredate",
            "termdate",
            "marital_status",
            "address_1",
            "address_2",
            "city",
            "state",
            "zip",
            "emp_status",
            "union_code",
            "er_pre",
            "er_post",
            "ee_pre",
            "ee_post",
            "loan_1",
            "loan_2",
            "loan_3",
            "loan_4",
            "loan_5",
            "loan_6",
            "loan_7",
            "loan_8",
            "loan_9",
            "hours",
            "gross",
            "ytd_er_pre",
            "ytd_er_post",
            "ytd_ee_pre",
            "ytd_ee_post",
            "ytd_loan_1",
            "ytd_loan_2",
            "ytd_load_3",
            "ytd_loan_4",
            "ytd_loan_5",
            "ytd_loan_6",
            "ytd_loan_7",
            "ytd_loan_8",
            "ytd_loan_9",
            "ytd_hours",
            "ytd_gross"
        ]
    },
    "greco_accrual_balance": {
        "columns": [
            "id",
            "employee",
            "rate",
            "length_of_service",
            "code",
            "accrual_rate",
            "start_date",
            "hours_used",
            "hours_available",
            "days_used",
            "days_available"
        ],
        "exact_match": [
            "id",
            "employee",
            "rate",
            "length_of_service",
            "code",
            "accrual_rate",
            "start_date",
            "hours_used",
            "hours_available",
            "days_used",
            "days_available"
        ],
        "timestamp": [
            "start_date"
        ],
        "date_range": [],
        "ints": [
            "id",
            "employee",
            "rate",
            "length_of_service",
            "code",
            "accrual_rate",
            "start_date",
            "hours_used",
            "hours_available",
            "days_used",
            "days_available"
        ]
    },
    "greco_anniversary_report": {
        "columns": [
            "id",
            "employee",
            "hire_date",
            "rehire_date",
            "adj_seniority",
            "seniority",
            "pay_rate",
            "address_1",
            "address_2",
            "city",
            "zip"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [
            "hire_date",
            "rehire_date"
        ],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_benefits_reconciliation_report": {
        "columns": [
            "employee",
            "id",
            "status",
            "title"
        ],
        "exact_match": [
            "employee",
            "id",
            "status",
            "title"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "employee",
            "id",
            "status",
            "title"
        ]
    },
    "greco_birthday_listing_report": {
        "columns": [
            "id",
            "employee",
            "birthday",
            "address_1",
            "address_2",
            "city",
            "state",
            "zip_code"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_check_register_report": {
        "columns": [
            "employee_id",
            "employee_name",
            "net_amount"
        ],
        "exact_match": [
            "employee_id"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "employee_id"
        ]
    },
    "greco_employee_listing_report": {
        "columns": [
            "employee",
            "id",
            "ssn",
            "emp_status",
            "emp_type",
            "sui",
            "pay_freq",
            "rate_salary",
            "rate_per"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_employee_rates_and_hire_dates_report": {
        "columns": [
            "company_id",
            "department",
            "last_first_mi",
            "hire_date",
            "rehire_date",
            "hourly_rate",
            "salary"
        ],
        "exact_match": [
            "company_id"
        ],
        "timestamp": [
            "hire_date",
            "rehire_date"
        ],
        "date_range": [],
        "ints": [
            "company_id"
        ]
    },
    "greco_i9_tracking_report": {
        "columns": [
            "last_name",
            "first_name",
            "id",
            "work_authorization_status",
            "uscis_number",
            "work_authorization_type",
            "expiration"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_new_hire_report": {
        "columns": [
            "id",
            "employee",
            "ssn",
            "hire_date",
            "change_reason",
            "term_date",
            "emp_status"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [
            "hire_date",
            "term_date"
        ],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_new_hire_term_report": {
        "columns": [
            "id",
            "employee",
            "ssn",
            "hire_date",
            "term_reason",
            "term_date",
            "emp_status"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [
            "hire_date",
            "term_date"
        ],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_retirement_plan_participation_report": {
        "columns": [
            "name",
            "id",
            "401k_rate_amount",
            "401k_calc",
            "401k_ytd_amount",
            "401cu_rate_amount",
            "401cu_calc",
            "401cu_ytd_amount",
            "4roth_rate_amount",
            "4roth_calc",
            "4roth_ytd_amount",
            "403b_rate_amount",
            "403b_calc",
            "403b_ytd_amount"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_seniority_report": {
        "columns": [
            "id",
            "employee",
            "hire_date",
            "rehire_date",
            "adj_seniority",
            "seniority"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [
            "hire_date",
            "rehire_date"
        ],
        "date_range": [],
        "ints": [
            "id"
        ]
    },
    "greco_union_report": {
        "columns": [
            "id",
            "employee",
            "ssn",
            "affiliation_date",
            "union_position",
            "initiation_collected",
            "dues_collected"
        ],
        "exact_match": [
            "id"
        ],
        "timestamp": [
            "affiliation_date"
        ],
        "date_range": [],
        "ints": [
            "id"
        ]
    }
}
