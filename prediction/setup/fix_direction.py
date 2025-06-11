from google.cloud import bigquery
import re

def update_directions():
    # Initialize BigQuery client
    client = bigquery.Client()
    
    # Piccadilly line station orders
    piccadilly_outbound = [
            'Between Acton Town and Turnham Green', 'Approaching Turnham Green', 'At Turnham Green Platform 3',
            'Left Turnham Green', 'Between Turnham Green and Ravenscourt Park', 'At Ravenscourt Park Platform 3',
            'Between Ravenscourt Park and Hammersmith', 'Approaching Hammersmith', 'Hammersmith area',
            'Left Hammersmith', 'Between Hammersmith and Barons Court', 'Approaching Barons Court',
        'At Barons Court Platform 3', 'Left Barons Court', 'Between Barons Court and Earl''s Court',
        'Approaching Earl''s Court', 'At Earl''s Court Platform 5', 'Between Earl''s Court and Gloucester Road',
            'Approaching Gloucester Road', 'At Gloucester Road Platform 5', 'Left Gloucester Road',
            'Approaching South Kensington', 'At South Kensington Platform 4', 'Left South Kensington',
            'Between South Kensington and Knightsbridge', 'Approaching Knightsbridge', 'At Knightsbridge Platform 1',
            'Left Knightsbridge', 'Between Knightsbridge and Hyde Park Corner', 'Approaching Hyde Park Corner',
            'At Hyde Park Corner Platform 1', 'Between Hyde Park Corner and Green Park', 'Approaching Green Park',
            'At Green Park Platform 2', 'Between Green Park and Piccadilly Circus', 'At Piccadilly Circus Platform 3',
            'Between Piccadilly Circus and Leicester Square', 'At Leicester Square Platform 2',
            'Between Leicester Square and Covent Garden', 'At Covent Garden Platform 2',
            'Between Covent Garden and Holborn', 'At Holborn Platform 4', 'Between Holborn and Russell Square',
        'At Russell Square Platform 1', 'Between Russell Square and King''s Cross'
    ]
    
    piccadilly_inbound = [
        'Between Caledonian Road and King''s Cross',
            'At Caledonian Road Platform 2', 'Between Holloway Road and Caledonian Road',
            'At Holloway Road Platform 1', 'Between Arsenal and Holloway Road',
            'At Arsenal Platform 2', 'Between Finsbury Park and Arsenal',
            'At Finsbury Park Platform 3', 'Between Manor House and Finsbury Park',
            'At Manor House Platform 1', 'Between Turnpike Lane and Manor House',
            'Approaching Turnpike Lane', 'At Turnpike Lane Platform 2', 'Left Turnpike Lane',
            'Between Wood Green and Turnpike Lane', 'Approaching Wood Green',
            'At Wood Green Platform 2', 'Left Wood Green',
            'Between Bounds Green and Wood Green', 'Approaching Bounds Green',
            'At Bounds Green Platform 1', 'Left Bounds Green',
            'Between Arnos Grove and Bounds Green', 'Approaching Arnos Grove',
            'At Arnos Grove Platform 4', 'Left Arnos Grove',
            'Between Southgate and Arnos Grove', 'Approaching Southgate',
            'At Southgate Platform 2', 'Left Southgate',
            'Between Oakwood and Southgate', 'Approaching Oakwood',
            'At Oakwood Platform 1', 'Left Oakwood',
            'Between Cockfosters and Oakwood'
        ]
    
    # Build the CASE statement for outbound stations
    outbound_cases = []
    for station in piccadilly_outbound:
        outbound_cases.append(f"WHEN LOWER(current_location) LIKE '%{station.lower()}%' THEN 'outbound'")
    
    # Build the CASE statement for inbound stations
    inbound_cases = []
    for station in piccadilly_inbound:
        inbound_cases.append(f"WHEN LOWER(current_location) LIKE '%{station.lower()}%' THEN 'inbound'")
    
    # Combine all cases
    all_cases = '\n'.join(outbound_cases + inbound_cases)
    
    # Update query for both tables
    update_query = f"""
    UPDATE `nico-playground-384514.transport_predictions.any_errors`
    SET direction = CASE 
        {all_cases}
    END
    WHERE direction IS NULL
    AND current_location IS NOT NULL
    AND line = 'piccadilly'
    """
    
    try:
        # Execute update for any_errors
        print("\nUpdating directions for Piccadilly line in any_errors...")
        update_job = client.query(update_query)
        update_job.result()  # Wait for the job to complete
        
        # Execute update for initial_errors
        print("\nUpdating directions for Piccadilly line in initial_errors...")
        initial_errors_query = update_query.replace('any_errors', 'initial_errors')
        initial_errors_job = client.query(initial_errors_query)
        initial_errors_job.result()  # Wait for the job to complete
        
        # Preview the changes in any_errors
        preview_query = """
        SELECT 
            train_id,
            line,
            current_location,
            direction
        FROM `nico-playground-384514.transport_predictions.any_errors`
        WHERE line = 'piccadilly'
        AND direction IS NOT NULL
        LIMIT 20
        """
        
        print("\nPreviewing updated records in any_errors:")
        print("--------------------------------")
        preview_job = client.query(preview_query)
        for row in preview_job:
            print(f"Train ID: {row.train_id}")
            print(f"Line: {row.line}")
            print(f"Current Location: {row.current_location}")
            print(f"Direction: {row.direction}")
            print("--------------------------------")
            
        # Preview the changes in initial_errors
        initial_preview_query = preview_query.replace('any_errors', 'initial_errors')
        print("\nPreviewing updated records in initial_errors:")
        print("--------------------------------")
        initial_preview_job = client.query(initial_preview_query)
        for row in initial_preview_job:
            print(f"Train ID: {row.train_id}")
            print(f"Line: {row.line}")
            print(f"Current Location: {row.current_location}")
            print(f"Direction: {row.direction}")
            print("--------------------------------")
            
    except Exception as e:
        print(f"Error updating directions: {str(e)}")

if __name__ == "__main__":
    update_directions()