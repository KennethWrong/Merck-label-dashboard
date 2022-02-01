from sqlalchemy import create_engine  
from sqlalchemy import Column, String, DateTime, Integer, Float
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
print(f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}/{pg_database}")
db = create_engine(f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}/{pg_database}") 
base = declarative_base()

def get_database_uri():
    return f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}/{pg_database}"

class Sample(base):  
    __tablename__ = 'samples'
    qr_code_key = Column(String, primary_key=True)
    sample_name = Column(String)
    test_round = Column(Integer)
    sample_consistency = Column(Float)
    analyst = Column(String)
    date_entered = Column(DateTime)
    date_modified = Column(DateTime)
    expiration_date = Column(DateTime)

#Initializing the DB
Session = sessionmaker(db) 
session = Session()
base.metadata.create_all(db)
