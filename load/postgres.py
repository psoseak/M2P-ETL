import pandas as pd
from connection.postgres_config import create_engine, dispose_engine


# Read from db and set it as data frame
def select_table(sql_query, schema):
    try:
        table = pd.read_sql_query(sql_query, create_engine(schema))
        return table
    except:
        return ''


# To insert to database
def upsert_table(data_frame, schema, table_name):
    engine = create_engine(schema)
    data_frame.to_sql(table_name, con=engine, if_exists='replace')

    # try to close connection
    dispose_engine(engine)


def test_retrieve_postgres():
    schema = 'wekan'
    table = 'table_name1'

    # Test on retrieving from postgres
    sql_query = "SELECT * FROM vendors"
    # sql_query = "SELECT version()"
    retrieved_info = select_table(sql_query, schema)
    print(retrieved_info)

    # Add one more row
    retrieved_info_new = retrieved_info.append({'vendor_id': '3', 'vendor_name': 'new name'}, ignore_index=True)
    print(retrieved_info_new)

    # upsert to table
    upsert_table(retrieved_info_new, schema, table)
