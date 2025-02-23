# ETL Pipeline Documentation

## Overview

This ETL (Extract, Transform, Load) pipeline is designed to fetch collections data from the OpenSea API, transform it to fit a structured database format, and load it into a PostgreSQL database using a custom ORM. Additionally, the raw data is stored in a data lake.

## Project Structure


```
project_root/
│-- handle_etl/
│   │-- __init__.py       # To import handle_etl files
│   │-- etl_pipeline.py   # Main ETL pipeline execution script
│   │-- extract.py        # Handles data extraction from OpenSea API
│   │-- transform.py      # Transforms raw data
│   │-- load_data.py      # Loads data into PostgreSQL
│-- database_app/
│   │-- base_model.py     # Base model that represents a table in database
│   │-- database.py       # Handles database connection.
│   │-- models.py         # Defines database models using custom ORM
│-- data_lake/
│   │-- raw_data.json     # Stores extracted raw data
│   │-- cleaned_data.json # Stores transformed data
│-- .env                  # Environment variables (API keys, DB credentials)
│-- run_scripts.py        # Playground for testing code
│-- requirements.txt      # Requirement packages
```

## ETL Process

### 1. Data Extraction

**File:** `handle_etl/extract.py`

- Uses the OpenSea Collections API (`/api/v2/collections`) to fetch NFT collections.
- Handles API rate limits.
- Stores the raw JSON response in `data_lake/raw_data.json`.

```python
from handle_etl.extract import fetch_collections
raw_data = fetch_collections()
```

### 2. Data Transformation

**File:** `handle_etl/transform.py`

- Loads raw data from `data_lake/raw_data.json`.
- Filters collections to include only those on the Ethereum blockchain.
- Maps and structures the data to fit the database schema.
- Saves the cleaned data to `data_lake/cleaned_data.json`.

```python
from handle_etl.transform import transform_data
transformed_data = transform_data()
```

### 3. Data Loading

**File:** `handle_etl/load_data.py`

- Uses the custom ORM to insert transformed data into PostgreSQL.
- Implements batch processing to optimize database inserts.

```python
from handle_etl.load_data import load_data
load_data(transformed_data)
```

### 4. Put Everything in run_scripts.py file

**File:** `run_scripts.py`

- Playground to test and run.

```python
from handle_etl.etl_pipeline import run_etl

if __name__ == "__main__":
    run_etl()
```

## Running the ETL Pipeline

Execute the ETL pipeline by running the following command:

```sh
python run_scripts.py
```

This will execute the following steps:

1. Extract data from OpenSea API.
2. Transform and filter Ethereum-based collections.
3. Load the transformed data into the PostgreSQL database.

## Table Schema

The data is loaded into a table with the following fields:

| Column             | Type | Description                                              |
| ------------------ | ---- | -------------------------------------------------------- |
| `collection`       | TEXT | The name of the collection                               |
| `name`             | TEXT | The name of the collection item                          |
| `description`      | TEXT | The description of the collection item                   |
| `image_url`        | TEXT | The URL of the image associated with the collection item |
| `owner`            | TEXT | The owner of the collection                              |
| `twitter_username` | TEXT | username of the owner of collection                      |
| `contracts`        | JSON | Details of the contracts associated with the collection  |

## Configuration

Set up the environment variables in a `.env` file:

```
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_pass

OPENSEA_API_KEY=your_api_key
```

## Dependencies

Install dependencies using:

```sh
pip install -r requirements.txt
```
