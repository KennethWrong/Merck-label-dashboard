from sqlalchemy import MetaData, Table, String, Column, Text, DateTime, Boolean, create_engine
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import os

##########################################################################################
# This file is just for the creation of our database along with the table 'samples'        #
##########################################################################################
db_path = os.path.join(os.getcwd(),'data','database.db')
engine = create_engine(f'sqlite:///{db_path}')
conn = engine.connect()

metadata = MetaData(bind=engine)


samples = Table('samples', metadata,
    Column('qr_code_key',String(50),primary_key=True),
    Column('sample_id',String(50), nullable=False),
    Column('batch_id', String(50), nullable=False),
    Column('protein_concentration',String(50)),
    Column('date_entered',Text(50),default=datetime.utcnow)
)

metadata.create_all(engine)
