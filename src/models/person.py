from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models import Base 

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    sex = Column(String(1))
    ssn = Column(String)
    title = Column(String)
    appointed = Column(Date)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # create one to many relation ship with company using foreign key
    company = relationship("Company", back_populates="people")


