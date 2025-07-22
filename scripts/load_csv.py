import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os
# PostgreSQL connection (local)
# Obs: I used Sqlachemy for faster load and conn to the Postgre*
engine = create_engine('postgresql+psycopg2://postgres:1581mcss!@localhost:5432/Northwind')

try:
    with engine.connect() as conn:
        print("Connected with Postgre!")
except Exception as err:
    print("Connection error! Verify your connection", err)

# Path 
data_northwind = 'C:/Users/Cunha/Documents/Northwind/data'

# List .csv files in the "./data_northwind"
csv_list = [f for f in os.listdir(data_northwind) if f.endswith('.csv')]

# Load each CSV into PostgreSQL
for file in csv_list:
    table_name = file.replace('.csv', '') 
    file_path = os.path.join(data_northwind, file) 
    df = pd.read_csv(file_path, sep=';')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Table {table_name} loaded into local PostgreSQL !")