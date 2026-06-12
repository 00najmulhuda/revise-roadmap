from sqlmodel import create_engine
from dotenv import load_dotenv
import os

#load .env file
load_dotenv()

#get DATABASE URL
DATABASE_URL = os.getenv("DATABASE_URL")

#CREATE_ENGINE
engine = create_engine(DATABSE_URL)

