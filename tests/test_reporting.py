
import sys
import os

# add absolute path to src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Market
from frontend.reporting import get_companies, get_active_years
from datetime import date


@pytest.fixture
def session():
    """fixture for in memory test db session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_get_companies_returns_data(session):
    # add mock data
    session.add(Company(name="Fake Company", figi="AAAAA1", lei="Z2222", address="12 ROAD", city="acity", state="XX", zip="00000"))
    session.commit()

    # replicate action 
    companies = get_companies(session)

    # assertion checks
    assert len(companies) == 1
    assert companies[0] == "Fake Company"

def test_get_active_years_returns_sorted_years(session):
    # Add company
    company = Company(name="Some Company", figi="BB123", lei="LEI123")
    session.add(company)
    session.commit()

    # Add market data for multiple years
    market_data = [
        Market(date=date(2021, 3, 1), last_price=100.0, figi="BB123", company_id=company.id),
        Market(date=date(2023, 7, 1), last_price=110.0, figi="BB123", company_id=company.id),
        Market(date=date(2022, 5, 1), last_price=105.0, figi="BB123", company_id=company.id),
    ]
    session.add_all(market_data)
    session.commit()

    # Call function
    years = get_active_years("Some Company", session)

    # Assertions
    assert years == [2023, 2022, 2021]
