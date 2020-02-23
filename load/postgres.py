import pandas as pd
from connection.postgres_config import create_engine_config, dispose_engine


# Read from db and set it as data frame
def select_table(sql_query, schema, db_properties):
    try:
        table = pd.read_sql_query(sql_query, create_engine_config(schema, db_properties))
        return table
    except:
        return ''


# To insert to database
def upsert_table(data_frame, schema, table_name, db_properties):
    engine = create_engine_config(schema, db_properties)
    data_frame.to_sql(table_name, con=engine, if_exists='replace')

    # Try to close connection
    dispose_engine(engine)


def test_retrieve_postgres(db_properties):
    schema = 'wekan'
    table = 'table_name_2'

    # Test on retrieving from postgres
    sql_query = 'SELECT * FROM vendors'
    # sql_query = "SELECT version()"]
    retrieved_info = select_table(sql_query, schema, db_properties)

    # Add one more row
    retrieved_info_new = retrieved_info.append({'vendor_id': '3', 'vendor_name': 'new name'}, ignore_index=True)
    print(retrieved_info_new)

    # Upsert to table
    upsert_table(retrieved_info_new, schema, table, db_properties)
