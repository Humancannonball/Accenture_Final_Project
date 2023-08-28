import os, pymongo
import snowflake.connector
from dotenv import load_dotenv
import pandas as pd
from functools import lru_cache

load_dotenv()

# Used to connect to Snowflake, execute queries.
class SnowflakeConnector:
    def __init__(self):
        self.snowflake_user = os.getenv('SNOWFLAKE_USER')
        self.snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
        self.snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        self.snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
        self.snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
        self.snowflake_conn = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account,
            warehouse=self.snowflake_warehouse,
            database=self.snowflake_database,
            schema=self.snowflake_schema
        )
    @lru_cache(maxsize=32)
    def execute_query(self, query):
        if not self.snowflake_conn:
            self.connect()
        cursor = self.snowflake_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        return df
    def get_filtered_df_by_country(self, country: str):
        return self.execute_query(f"SELECT COUNTRY_REGION,PROVINCE_STATE,DEATHS,CONFIRMED,INCIDENT_RATE FROM JHU_DASHBOARD_COVID_19_GLOBAL WHERE COUNTRY_REGION = '{country}' limit 15;")
        
    
# Used to connect to MongoDB, execute queries.
class MongoConnector:
    def __init__(self): 
        self.connection_string = os.getenv('CONNECTION_STRING')
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client['additional_data']
        self.collection = self.db['gdp']
        
    def get_countries(self):
        return self.collection.distinct('Country Name')
  
    @lru_cache(maxsize=32)
    def get_filtered_df_by_country(self, country: str):
        rows = self.collection.find({'Country Name': country})
        data = [row for row in rows]
        df = pd.DataFrame(data)
        return df
    
        