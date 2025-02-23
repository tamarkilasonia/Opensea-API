from .database import Database
import logging

logging.basicConfig(level=logging.ERROR)


class QuerySet(list):
    def __init__(self, model, condition_str, values, objects):
        """
        :param model: The Model subclass (e.g. Collection)
        :param condition_str: The SQL fragment for WHERE clause ("name = %s AND description ILIKE %s")
        :param values: A list (or tuple) of values corresponding to the placeholders in condition_str (%Modern Art Collection%).
        :param objects: The list of model instances retrieved from the SELECT query.
        """
        super().__init__(objects)  # Initialize as a list with the fetched objects.
        self.model = model
        self.condition_str = condition_str  # Stored condition (without the 'WHERE' keyword)
        self.values = values  # Stored values for the SQL placeholders

    def delete(self):
        """
        Deletes all records from the database that match the stored condition.
        If no condition is set (empty string), it deletes all records in the table.
        """

        if self.condition_str:
            sql = f"DELETE FROM {self.model.__name__.lower()} WHERE {self.condition_str}"
        else:
            # delete all records
            sql = f"DELETE FROM {self.model.__name__.lower()}"

        try:
            self.model.db.execute(sql, tuple(self.values))

            # clear the list
            self.clear()
        except Exception as e:
            logging.error(f"Error deleting records in {self.model.__name__.lower()}: {e}")

    def order_by(self, order_by_keyword):
        """
        Order objects by specific keyword.
        """

        ord_direction = "ASC"

        field = order_by_keyword

        if order_by_keyword.startswith("-"):
            ord_direction = "DESC"
            field = order_by_keyword[1:]

        if field not in self.model.__annotations__:
            logging.error(f"Invalid order_by field '{field}' for model {self.model.__name__.lower()}")
            return None

        if self.condition_str:
            sql = f"""
            SELECT * FROM {self.model.__name__.lower()}
            WHERE {self.condition_str}
            ORDER BY {order_by_keyword} {ord_direction}
        """
        else:
            sql = f"SELECT * FROM {self.model.__name__.lower()} ORDER BY {order_by_keyword} {ord_direction}"

        try:
            results = self.model.db.fetch(sql, tuple(self.values))

            objects = [self.model(**dict(zip(["id"] + list(self.model.__annotations__.keys()), row))) for row in
                       results]

            # clear the list
            self.clear()

            return QuerySet(self.model, self.condition_str, self.values, objects)
        except Exception as e:
            logging.error(f"Error while ordering items in {self.model.__name__.lower()}: {e}")

    def limit(self, limit):
        """
        Limit objects.
        """

        if type(limit) is not int:
            return logging.error("Please provide integer for limitation")

        if self.condition_str:
            sql = f"""
            SELECT * FROM {self.model.__name__.lower()}
            WHERE {self.condition_str}
            LIMIT {limit}
        """
        else:
            sql = f"SELECT * FROM {self.model.__name__.lower()} LIMIT {limit}"

        try:
            results = self.model.db.fetch(sql, tuple(self.values))

            objects = [self.model(**dict(zip(["id"] + list(self.model.__annotations__.keys()), row))) for row in
                       results]

            # clear the list
            self.clear()

            return QuerySet(self.model, self.condition_str, self.values, objects)
        except Exception as e:
            logging.error(f"Error while ordering items in {self.model.__name__.lower()}: {e}")

    def update(self, **fields):
        """
        Update all records or records based on some conditions.
        """

        if not fields:
            return logging.error(f"Please provide key, value to update records")

        table_name = self.model.__name__.lower()

        set_clauses = []
        parameters = []

        for key, value in fields.items():
            if key not in self.model.__annotations__:
                logging.error(f"'{key}' is not a valid field in {table_name}")
                return
            # Use a placeholder for each value.
            set_clauses.append(f"{key} = %s")
            parameters.append(value)

        set_clause_str = ", ".join(set_clauses)

        if self.condition_str:
            sql = f"""
                UPDATE {table_name}
                SET {set_clause_str}
                WHERE {self.condition_str}
            """
            # Append the condition values after the new parameters.
            parameters.extend(self.values)
        else:
            sql = f"""
                UPDATE {table_name}
                SET {set_clause_str}
            """

        try:
            self.model.db.execute(sql, tuple(parameters))
            self.clear()
        except Exception as e:
            logging.error(f"Error updating records in {table_name}: {e}")


class Model:
    db = Database()

    def __init__(self, **kwargs):
        """
        Initialize the instance with dynamic attributes.
        """

        # name="Name"
        # description="Description"...

        for field in self.__annotations__:
            setattr(self, field, kwargs.get(field, None))

    @classmethod
    def create_table(cls):
        """Generate and execute SQL to create table based on fields"""
        try:
            fields = []
            for field_name, field_type in cls.__annotations__.items():
                sql_type = cls.get_sql_type(field_type)
                fields.append(f"{field_name} {sql_type}")

            # fields: ['collection TEXT', 'name TEXT', 'description TEXT', 'image_url TEXT', 'owner TEXT', 'twitter_username TEXT', 'contracts JSONB']

            sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} (
                id SERIAL PRIMARY KEY,
                {', '.join(fields)}
            )
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error creating table {cls.__name__.lower()}: {e}")

    @classmethod
    def drop_table(cls):
        """Generate and execute SQL to drop table"""
        try:

            sql = f"""
            DROP TABLE IF EXISTS {cls.__name__.lower()}
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error while drop table {cls.__name__.lower()}: {e}")

    @classmethod
    def remove_columns(cls, *columns):
        """Removes specified columns from the table."""
        try:
            if not columns:
                logging.error("No columns specified for removal.")
                return

            alter_statements = [f"DROP COLUMN IF EXISTS {col}" for col in columns]
            sql = f"""
            ALTER TABLE {cls.__name__.lower()}
            {', '.join(alter_statements)}
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error removing columns from {cls.__name__.lower()}: {e}")

    @classmethod
    def modify_column_type(cls, column_name, new_type):
        """Changes the data type of an existing column."""
        try:
            sql = f"""
            ALTER TABLE {cls.__name__.lower()}
            ALTER COLUMN {column_name} TYPE {new_type}
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error modifying column {column_name} in {cls.__name__.lower()}: {e}")

    @classmethod
    def add_new_column(cls, column_name, data_type):
        """Add new column."""
        try:
            sql = f"""
            ALTER TABLE {cls.__name__.lower()}
            ADD COLUMN {column_name} {data_type}
            """
            cls.db.execute(sql)
        except Exception as e:
            logging.error(f"Error adding column {column_name} in {cls.__name__.lower()}: {e}")

    @staticmethod
    def get_sql_type(field_type):
        """Map Python types to PostgreSQL types"""
        if field_type == str:
            return "TEXT"
        elif field_type == int:
            return "INTEGER"
        elif field_type == float:
            return "REAL"
        elif field_type == dict:
            return "JSONB"
        else:
            return "TEXT"

    # we don't need classmethod here because we are working for only one instance and we want this code to work only for it.
    def save(self):
        """Insert the current object into the database"""

        try:
            # self.__annotations__ is collection model dict {'name': <class 'str'>}

            fields = [f for f in self.__annotations__ if f != "id"]
            values = [getattr(self, f) for f in fields]

            # print(values) ['Art NFTs', 'Modern Art Collection',  'nft_artist', {'main': '0xabcdef...'}]
            # print(fields)

            # we are making a placeholders for values with {', '.join(['%s']*len(values))}

            sql = f"""
            INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)})
            VALUES ({', '.join(['%s'] * len(values))})
            """

            # INSERT INTO collection (name, description, image_url)
            #    VALUES (%s, %s, %s)

            self.db.execute(sql, values)
        except Exception as e:
            logging.error(f"Error saving record in {self.__class__.__name__.lower()}: {e}")

    # we need to operate multiple instances so we are using classmethod to work on any subclass.
    @classmethod
    def bulk_insert(cls, objects):
        """Insert multiple records at once for better efficiency"""
        if not objects:
            return  # No data to insert

        try:
            fields = [f for f in cls.__annotations__ if f != "id"]

            # instead of one list now we are getting multiple lists of values
            values_list = [[getattr(obj, f) for f in fields] for obj in objects]

            sql = f"""
            INSERT INTO {cls.__name__.lower()} ({', '.join(fields)})
            VALUES ({', '.join(['%s'] * len(fields))})
            """

            flattened_values = [tuple(item) for item in values_list]

            # flattened values: flattened_values = [
            #    "Bored Ape", "NFT collection", "some_url",
            #    "CryptoPunks", "Another NFT", "another_url"
            # ]

            cls.db.executemany(sql, flattened_values)
        except Exception as e:
            logging.error(f"Error in bulk insert for {cls.__name__.lower()}: {e}")

    @classmethod
    def all(cls):
        """Retrieve all records from the table"""

        try:
            sql = f"SELECT * FROM {cls.__name__.lower()}"

            results = cls.db.fetch(sql)

            # creates a list of key names: zip(["id"] + list(cls.__annotations__.keys()
            # row represents the one row of the data that fetched: (1, "Art NFTs", "Modern Art Collection", "A collection of modern NFT artworks.",...
            # with zip we pair kay names and values
            # converts list of tuple into a dict: dict(zip(...))
            # with cls we create collection instances from dicts.

            objects = [cls(**dict(zip(["id"] + list(cls.__annotations__.keys()), row))) for row in results]

            return QuerySet(cls, "", "", objects)

        except Exception as e:
            logging.error(f"Error fetching all records from {cls.__name__.lower()}: {e}")
            return []

    @classmethod
    def filter(cls, **conditions):
        """Filter records based on conditions and return a QuerySet object."""
        try:
            condition_clauses = []
            values = []

            for key, value in conditions.items():
                lower_dash_idx = key.find("__")
                if lower_dash_idx == -1:
                    field = key
                    operation = "equals"
                else:
                    field = key[:lower_dash_idx]
                    operation = key[lower_dash_idx + 2:]

                if operation == "icontains":
                    condition_clauses.append(f"{field} ILIKE %s")
                    values.append(f"%{value}%")
                elif operation == "contains":
                    condition_clauses.append(f"{field} LIKE %s")
                    values.append(f"%{value}%")
                else:
                    condition_clauses.append(f"{field} = %s")
                    values.append(value)

            # Join conditions using AND. (If no conditions are provided, condition_str will be empty.)
            condition_str = " AND ".join(condition_clauses)

            sql = f"SELECT * FROM {cls.__name__.lower()}"
            if condition_str:
                sql += f" WHERE {condition_str}"

            results = cls.db.fetch(sql, tuple(values))
            objects = []
            for row in results:
                # Create model instances from the fetched row.
                data = dict(zip(["id"] + list(cls.__annotations__.keys()), row))
                objects.append(cls(**data))

            # Return a QuerySet, which is a list with extra methods.
            return QuerySet(cls, condition_str, values, objects)

        except Exception as e:
            logging.error(f"Error filtering records in {cls.__name__.lower()}: {e}")
            return QuerySet(cls, "", [], [])