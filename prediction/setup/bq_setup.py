from google.cloud import bigquery
from google.api_core import exceptions

client = bigquery.Client()
dataset_id = "transport_predictions"

# First drop existing tables
for table_name in ['prediction_history', 'initial_errors', 'any_errors']:
    try:
        client.delete_table(f"{client.project}.{dataset_id}.{table_name}")
        print(f"Dropped table {table_name}")
    except exceptions.NotFound:
        print(f"Table {table_name} does not exist")

# Create tables with proper schema
schema = {
    'prediction_history': [
        bigquery.SchemaField("train_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("line", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("time_to_station", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("current_location", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("initial_prediction_timestamp", "TIMESTAMP"),
        bigquery.SchemaField("any_prediction_timestamp", "TIMESTAMP"),
        bigquery.SchemaField("arrival_timestamp", "TIMESTAMP"),
    ],
    'initial_errors': [
        bigquery.SchemaField("train_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("line", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("initial_prediction_timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("arrival_timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("error_seconds", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("time_to_station", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("hour", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("day_of_week", "INTEGER", mode="REQUIRED"),
    ],
    'any_errors': [
        bigquery.SchemaField("train_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("line", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("any_prediction_timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("arrival_timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("error_seconds", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("time_to_station", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("hour", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("day_of_week", "INTEGER", mode="REQUIRED"),
    ]
}

# Create tables with clustering and primary keys
for table_name, table_schema in schema.items():
    table = bigquery.Table(f"{client.project}.{dataset_id}.{table_name}", schema=table_schema)
    
    # Add clustering fields
    if table_name in ['initial_errors', 'any_errors']:
        table.clustering_fields = ["line", "train_id"]
    
    # Create the table
    try:
        table = client.create_table(table)
        print(f"Created table {table_name}")
        
        # Add primary keys
        if table_name == 'initial_errors':
            query = f"""
            ALTER TABLE `{client.project}.{dataset_id}.{table_name}`
            ADD PRIMARY KEY(train_id, initial_prediction_timestamp) NOT ENFORCED;
            """
            client.query(query).result()
        elif table_name == 'any_errors':
            query = f"""
            ALTER TABLE `{client.project}.{dataset_id}.{table_name}`
            ADD PRIMARY KEY(train_id, any_prediction_timestamp) NOT ENFORCED;
            """
            client.query(query).result()
        print(f"Added primary key to {table_name}")
    except Exception as e:
        print(f"Error creating table {table_name}: {e}")