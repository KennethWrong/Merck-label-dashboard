import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
import os

load_dotenv()
pg_host = os.getenv('POSTGRES_HOST')
pg_database = os.getenv('POSTGRES_DATABASE')
pg_username = os.getenv('POSTGRES_USERNAME')
pg_password = os.getenv('POSTGRES_PASSWORD')
pg_port = os.getenv('POSTGRES_PORT')

#http://jf-postgres-test-server.postgres.database.azure.com
#azure_admin
#tU!fE1ys38Pi

#Your username and password
db_uri = f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
db = create_engine(db_uri) 

if not database_exists(db.url):
    create_database(db.url)

conn = db.connect()
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

if not db.dialect.has_table(conn, "samples"):
    meta = MetaData(db)  
    sample_table = Table('samples', meta,  
                           Column('qr_code_key', String, primary_key=True),
                           Column('experiment_id', String, nullable=False),
                           Column('storage_condition', String, nullable=False),
                           Column('contents', String, nullable=False),
                           Column('analyst', String, nullable=False),
                           Column('date_entered', Date, nullable=False),
                           Column('date_modified', Date, nullable=False),
                           Column('expiration_date', Date, nullable=False),
                           )

    meta.create_all()

    s1 = Sample(qr_code_key="123", experiment_id="123", storage_condition="Cold", 
    contents="123 degrees", analyst="Joe", date_entered=datetime.date(2021, 10, 24), 
    date_modified=datetime.date(2021, 10, 24), expiration_date=datetime.date(2021, 10, 24))
   
    s2 = Sample(qr_code_key="124", experiment_id="12345", storage_condition="Cold cold", 
    contents="123 degrees", analyst="Joe", date_entered=datetime.date(2021, 10, 24), 
    date_modified=datetime.date(2021, 10, 24), expiration_date=datetime.date(2021, 10, 24))

    s3 = Sample(qr_code_key="125", experiment_id="12345", storage_condition="Cold hot", 
    contents="123 degrees", analyst="Joe", date_entered=datetime.date(2021, 10, 24), 
    date_modified=datetime.date(2021, 10, 24), expiration_date=datetime.date(2021, 10, 24))
    
    with Session(db) as session:
        session.add_all([s1, s2, s3])


def get_database_uri():
    return db_uri

