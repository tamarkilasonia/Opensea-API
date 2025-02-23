from handle_etl.load_data import load_data
from handle_etl.exctract import fetch_collections
from handle_etl.transform import transform_data

def run_etl():
    """Execute the full ETL pipeline: Extract → Transform → Load."""
    print("Starting ETL Process...")

    print("Extracting data from OpenSea API...")
    raw_data = fetch_collections()
    print(f"Extracted {len(raw_data)} records.")

    print("Transforming data...")
    transformed_data = transform_data()
    print(f"Transformed {len(transformed_data)} records.")

    print("Loading data into PostgreSQL...")
    load_data(transformed_data)

    print("ETL Process Completed Successfully!")