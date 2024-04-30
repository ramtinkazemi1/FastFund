from flask import Flask
from sqlalchemy import create_engine, Column, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URI"))

Session = sessionmaker(bind=engine)
FastFund_db = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    phone_number = Column(String(20), primary_key=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    balance = Column(Numeric(15, 2), default=0.00)


from routes import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(port=5000)


