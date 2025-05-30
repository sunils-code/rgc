from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from models import Base 


class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    figi = Column(String)
    last_price = Column(Float)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # create one to many relation ship with company using foreign key
    company = relationship("Company", back_populates="market")