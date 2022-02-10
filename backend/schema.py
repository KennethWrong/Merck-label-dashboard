from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from  sqlalchemy.orm import sessionmaker
import os

load_dotenv()
pg_host = os.getenv('POSTGRES_HOST')
pg_database = os.getenv('POSTGRES_DATABASE')
pg_username = os.getenv('POSTGRES_USERNAME')
pg_password = os.getenv('POSTGRES_PASSWORD')

#Your username and password
db = create_engine(f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}/{pg_database}") 
base = declarative_base()

def get_database_uri():
    return f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}/{pg_database}"

class Sample(base):  
    __tablename__ = 'samples'
    qr_code_key = Column(String, primary_key=True)
    experiment_id = Column(String)
    storage_condition = Column(String)
    analyst = Column(String)
    contents = Column(String)
    date_entered = Column(Date)
    date_modified = Column(Date)
    expiration_date = Column(Date)

#Initializing the DB
Session = sessionmaker(db) 
session = Session()
base.metadata.create_all(db)
