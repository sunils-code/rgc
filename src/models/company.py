from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    figi = Column(String)
    lei = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    formed = Column(Date)


