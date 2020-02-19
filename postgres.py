import psycopg2
import pandas as pd
import sqlalchemy as sa
import io

# Obtain the configuration parameters
from connection.postgres_config import config

params = config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
# Create a new cursor
cur = conn.cursor()


# A function that takes in a PostgreSQL query and outputs a pandas database
def create_pandas_table(sql_query, database=conn):
    table = pd.read_sql_query(sql_query, database)
    return table


# To insert to database
def update_table(dataframe, schema, table_name):
    engine = sa.create_engine("postgresql+psycopg2://root:VMware1!@localhost:54320/postgres",
                              connect_args={'options': '-csearch_path={}'.format(schema)})

    dataframe.head(0).to_sql(table_name, engine, if_exists='replace', index=False)  # truncates the table

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    dataframe.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, table_name, null="")  # null values become ''
    conn.commit()


    # pd.io.sql.to_sql(new_df, 'stg.temp_20170731', conn,
    #                  if_exists='replace', index=False, chunksize=10)


# Utilize the create_pandas_table function to create a Pandas data frame
# Store the data as a variable
vendor_info = create_pandas_table("SELECT * FROM wekan.vendors")
vendor_info.info()
# Add one more row
vendor_info_new = vendor_info.append({'vendor_id': '3', 'vendor_name': 'new nane'}, ignore_index=True)
print(vendor_info_new)

# insert to table
schema = 'wekan'
table = 'table_name1'
update_table(vendor_info_new, schema, table)

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()
