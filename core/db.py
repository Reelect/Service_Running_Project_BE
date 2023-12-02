from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
import dotenv

dotenv.load_dotenv(verbose=True)

SQLALCHEMY_DATABASE_URL = environ["HUNTREASURE_DATABASE_URL"]
# format : "사용하는db://{username}:{password}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
