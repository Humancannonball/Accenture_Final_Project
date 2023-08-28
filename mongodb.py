from dotenv import load_dotenv
import os, pymongo
import pandas as pd

def mongodb_prepation():
    load_dotenv()
    connection_string = os.getenv('CONNECTION_STRING')
    # read and filter data, convert to suitable format
    df = pd.read_csv('gdp.csv')
    df_filtered = df[['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']]
    df_filtered.to_csv('gdp_filtered.csv', index=False)
    data = df_filtered.to_dict(orient='records')

    # establish connection, insert data
    client = pymongo.MongoClient(connection_string)
    db = client['additional_data']
    collection = db['gdp']
    collection.insert_many(data)


if __name__ == '__main__':
    mongodb_prepation()

