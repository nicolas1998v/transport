from google.cloud import bigquery

client = bigquery.Client()

# Add current_location column to all tables
tables = ['prediction_history']
for table in tables:
    try:
        # Add the column
        query = f"""
        ALTER TABLE `nico-playground-384514.transport_predictions.{table}`
        ADD COLUMN direction STRING;
        """
        client.query(query).result()
        print(f"Added direction column to {table}")
        
        # Set existing rows to NULL
        query = f"""
        UPDATE `nico-playground-384514.transport_predictions.{table}`
        SET direction = NULL
        WHERE direction IS NULL;
        """
        client.query(query).result()
        print(f"Set existing rows to NULL in {table}")
        
    except Exception as e:
        print(f"Error modifying {table}: {e}")