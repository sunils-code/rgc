from sqlalchemy import Column, Integer, String, Date
from models import Base
from sqlalchemy.orm import relationship

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

    # create one to many relation ship with persom
    # if a company is deleted all people linked are removed
    people = relationship("Person", back_populates="company", cascade="all, delete-orphan")

    # create one to many relation ship with market
    # if a company is deleted all market data linked are removed
    market = relationship("Market", back_populates="company", cascade="all, delete-orphan")


