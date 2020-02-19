import psycopg2
import pandas as pd
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
    print(table)
    return table


# Utilize the create_pandas_table function to create a Pandas data frame
# Store the data as a variable
vendor_info = create_pandas_table("SELECT * FROM wekan.vendors")
vendor_info
print(vendor_info.size)

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()
