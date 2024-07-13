from google.cloud import bigquery
from google.oauth2 import service_account

# Replace these variables with your actual file paths and project details
credentialsPath = r"C:/Users/yethu/Downloads/projecttransformed-d34992713caa.json"
project_id = 'projecttransformed'

datasets = {
    "department_schema": "department_schema.department_table",
    "employee_schema": "employee_schema.employee_table",
    "project_schema": "project_schema.project_table",
    "resource_utilisation_schema": "resource_utilisation_schema.resource_utilisation_table",
    "time_schema": "time_schema.time_table"
}

csv_files = {
    "department_schema": 'department_schema.csv',
    "employee_schema": 'employee_schema.csv',
    "project_schema": 'project_schema.csv',
    "resource_utilisation_schema": 'resource_utilisation_schema.csv',
    "time_schema": 'time_schema.csv'
}

credentials = service_account.Credentials.from_service_account_file(credentialsPath)
client = bigquery.Client(credentials=credentials, project=project_id)

for dataset, table in datasets.items():
    table_id = f"{project_id}.{table}"
    file_path = csv_files[dataset]

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter=",",
        skip_leading_rows=1,
    )

    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")
