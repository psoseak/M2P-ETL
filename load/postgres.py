import pandas as pd
import sqlalchemy as sa


def dispose_engine(engine):
    engine.dispose()


def create_engine(schema):
    # engine+driver
    engine = sa.create_engine("postgresql+psycopg2://root:VMware1!@localhost:54320/postgres",
                              connect_args={'options': '-csearch_path={}'.format(schema)})
    return engine


# Read from db and set it as data frame
def select_table(sql_query):
    try:
        table = pd.read_sql_query(sql_query, create_engine('wekan'))
        return table
    except:
        return ''


# To insert to database
def upsert_table(data_frame, schema, table_name):
    engine = create_engine(schema)
    data_frame.to_sql(table_name, con=engine, if_exists='replace')

    # try to close connection
    engine.dispose()


def test_retrieve_postgres():
    # Test on retrieving from postgres
    sql_query = "SELECT * FROM vendors"
    # sql_query = "SELECT version()"
    retrieved_info = select_table(sql_query)
    print(retrieved_info)

    # Add one more row
    retrieved_info_new = retrieved_info.append({'vendor_id': '3', 'vendor_name': 'new nane'}, ignore_index=True)
    print(retrieved_info_new)

    # upsert to table
    schema = 'wekan'
    table = 'table_name1'
    upsert_table(retrieved_info_new, schema, table)
