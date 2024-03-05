# Import necessary modules from sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the URL for the SQLAlchemy database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# Create a new engine instance at the database URL
# connect_args={'check_same_thread': False} is used to allow the 
# engine to be used in a multithreaded context
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, 
                       connect_args={'check_same_thread': False})

# Create a sessionmaker instance with autocommit and autoflush set to False
# bind=engine means that all sessions created with this sessionmaker will 
# be bound to this engine
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

# Create a base class for declarative models
Base = declarative_base()