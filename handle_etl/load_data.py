from database_app.models import Collection


def load_data(transformed_data, batch_size=100):
    """Load transformed data into PostgreSQL using batch insertion."""

    # Collection.create_table()

    total_records = len(transformed_data)

    # ensure 100 record will process at a time
    # i = 0, 100, 200 ...
    for i in range(0, total_records, batch_size):
        # extract next batch of data: [0:100], [100:200] ...
        batch = transformed_data[i: i + batch_size]

        collection_objects = [Collection(**data) for data in batch]

        Collection.bulk_insert(collection_objects)

    print(f"Successfully inserted {total_records} records into the database.")