from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from  sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

load_dotenv()
pg_host = os.getenv('POSTGRES_HOST')
pg_database = os.getenv('POSTGRES_DATABASE')
pg_username = os.getenv('POSTGRES_USERNAME')
pg_password = os.getenv('POSTGRES_PASSWORD')
pg_port = ':'+os.getenv('POSTGRES_PORT')

#Your username and password
db_uri = f"postgresql://{pg_username}:{pg_password}@{pg_host}{pg_port}/{pg_database}"
db = create_engine(db_uri) 

if not database_exists(db.url):
    create_database(db.url)

base = declarative_base()

#Schema of our database
class Sample(base):  
    __tablename__ = 'samples'
    qr_code_key = Column(String, primary_key=True)
    experiment_id = Column(String, nullable=False)
    storage_condition = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    analyst = Column(String, nullable = False)
    date_entered = Column(Date, nullable=False)
    date_modified = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)

def get_database_uri():
    return db_uri

####UNCOMMENT THIS BLOCK IF RUNNING DB FOR THE FIRST TIME####
#
# Initializing the DB
Session = sessionmaker(db) 
session = Session()
base.metadata.create_all(db)
#
############################################################
