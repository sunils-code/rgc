from sqlalchemy import Column, Integer, String, ForeignKey
from models import Base
from sqlalchemy.orm import relationship

class FinancialStatement(Base):

    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quarter = Column(String)
    revenue = Column(Integer)
    expenses = Column(Integer)
    net_income = Column(Integer)
    assets = Column(Integer)
    liabilities = Column(Integer)
    equity = Column(Integer)
    cash = Column(Integer)
    debt = Column(Integer)
    equity_ratio = Column(Integer)
    debt_ratio = Column(Integer)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates="financial_statements")