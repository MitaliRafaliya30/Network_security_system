#This Python script is designed to extract data from a CSV file, convert it to JSON format, and insert it into a MongoDB database. 

import os
import sys
import json
import certifi  # it used to make secure http connection (ensure HTTPS connections use secure and verified certificate authority)
import pandas as pd
import numpy as np
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from dotenv import load_dotenv   #used to load environment variables from .env file

# 2.  Loading MongoDB Connection String from Environment Variables (.env)
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


#MongoDB Atlas requires a secure SSL/TLS connection.
#Sometimes, your system’s default CA certificates may be outdated or missing.
#certifi.where() returns the file path of the trusted CA bundle used for SSL verification.
ca=certifi.where()


class NetworkDataExtract():
    # captures any errors encountered during initialization(creation of the class).
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    #CSV to JSON Converter    
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path) ## Load CSV into a Pandas DataFrame
            data.reset_index(drop=True,inplace=True)   # Reset index
            records=list(json.loads(data.T.to_json()).values())     # Convert DataFrame to JSON 
            return records  # return JSON data
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # Insert Data into MongoDB    
    # paras : records =  A list of JSON records to be inserted into MongoDB.
              # database = name of database
              # collection = name of collection (table-like structure)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) # creates a client to connect to MongoDB.
            self.database = self.mongo_client[self.database]  # Accesses the MongoDB database using the name stored in self.database.
            
            self.collection=self.database[self.collection] # Select collection from the database
            self.collection.insert_many(self.records)  # Insert JSON data into collection
            return(len(self.records))  # Return number of inserted records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

# entery point of the script     
if __name__=='__main__':
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="Network_security_db"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()  # create object of the NetworkDataExtract class
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        

