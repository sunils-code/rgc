import sys
import os

# add the parent directory (src) to python's module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, extract
import pandas as pd
from config import config
from models import Company, Market, Person, FinancialStatement
import plotly.graph_objects as go

# db setup
engine = create_engine(config["SQLITE_URI"])
Session = sessionmaker(bind=engine)

def get_companies(session):
    """return all companies, will be used to filter dashboard"""

    companies = session.query(Company).all()

    return sorted([c.name for c in companies])

def get_active_years(company_name, session):
    """return all active market years where  """
    
    # get company 
    company = session.query(Company).filter_by(name = company_name).first()

    # query for all years from market date
    years = (
        session.query(extract("year",Market.date))
        .filter(Market.company_id == company.id)
        .distinct()
        .all())
    
    # return sorted list of years
    return sorted([int(y[0]) for y in years], reverse=True)

def get_reporting_data(company_name, year, session):

    # filter for company
    company =  session.query(Company).filter_by(name=company_name).first()

    # load filtered company into dict
    company_data = {
        "name": company.name,
        "figi": company.figi,
        "lei": company.lei,
        "address": company.address,
        "city": company.city,
        "state": company.state,
        "zip": company.zip,
        "formed": company.formed
        
    }

    # get people relevant to company
    people = session.query(Person).filter_by(company_id = company.id).all()

    # Market data for the year
    market_data = (
        session.query(Market)
        .filter(
            Market.company_id == company.id,
            extract("year", Market.date) == year
        )
        .order_by(Market.date)
        .all()
    )

    market_df = pd.DataFrame([{
        "date": m.date,
        "last_price": m.last_price
    } for m in market_data])

    financials = (
        session.query(FinancialStatement).
        filter(
        FinancialStatement.company_id == company.id,
        FinancialStatement.quarter.like(f"%{year}")
        )
        .all()
        )
    
    financial_df = pd.DataFrame([{
        "quarter": f.quarter,
        "revenue": f.revenue,
        "expenses": f.expenses,
        "net_income": f.net_income,
        "assets": f.assets,
        "liabilities": f.liabilities,
        "equity": f.equity,
        "cash": f.cash,
        "debt": f.debt,
        "equity_ratio": f.equity_ratio,
        "debt_ratio": f.debt_ratio
    } for f in financials])

    
    return {
        "company": company_data,
        "people": people,
        "market_data": market_df,
        "financials": financial_df
    }

def plot_stock_price(market_df):
    """ normalise stock prices to 100 and plots them."""
    if market_df.empty:
        return go.Figure()

    # create copy as we dont want to modify the actual data 
    market_df = market_df.copy()
    market_df["normalised"] = market_df["last_price"] / market_df["last_price"].iloc[0] * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=market_df["date"],
        y=market_df["normalised"],
        mode="lines",
        name="Stock Price"
    ))

    fig.update_layout(
        title="Stock Price (Starting Price 100)",
        xaxis_title="Date",
        yaxis_title="Price (normalised)",
        template="plotly_white"
    )

    return fig
