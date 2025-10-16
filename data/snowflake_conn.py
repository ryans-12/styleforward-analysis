import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os

'''def connect_db():
    # Load environment variables from .env file
    load_dotenv()

    #Retrieve values
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    role = os.getenv("SNOWFLAKE_ROLE")

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )

    # Create a cursor object
    cur = conn.cursor()
    return cur,conn'''


'''def import_to_pandas(conn, sql_query):
    #takes conn and sql query as paramaters, imports them into dataframe and returns dataframe
    cur = conn.cursor().execute(sql_query)
    df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
    return df'''

'''def main():
    cur,conn = connect_db()
    #load any needed tables into CSVs
    orders_df = import_to_pandas(conn, "SELECT * from transactions")

    cur.close()
    conn.close()

    print(orders_df)'''

def import_to_pandas(sql_query):
    # Load environment variables from .env file
    load_dotenv()

    #Retrieve values
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    role = os.getenv("SNOWFLAKE_ROLE")

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )

    '''takes conn and sql query as paramaters, imports them into dataframe and returns dataframe'''
    cur = conn.cursor().execute(sql_query)
    df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
    return df

#transactions = import_to_pandas("Select * from customer_touchpoints")

