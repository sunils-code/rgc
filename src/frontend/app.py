import sys
import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# path and imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config
from frontend.reporting import get_companies, get_active_years, get_reporting_data, plot_stock_price

# db setup
engine = create_engine(config["SQLITE_URI"])
Session = sessionmaker(bind=engine)
session = Session()

# streamlit
st.set_page_config(page_title="Company Annual Report", layout="wide")
st.title("📈 Company Annual Reporting Dashboard")

# select company
companies = get_companies(session)
company_name = st.selectbox("Select a company", companies)

# select year on active years
if company_name:
    years = get_active_years(company_name, session)
    year = st.selectbox("Select a year", years)

    if year:
        st.subheader(f"📄 Annual Report for {company_name} - {year}")
        report = get_reporting_data(company_name, year, session)

        # company Profile
        st.markdown("### 🏢 Company Profile")
        company_info = report["company"]
        st.write(pd.DataFrame(company_info.items()))

        # notable People
        st.markdown("### 👥 Notable People")
        people = report["people"]
        if people:
            st.table(pd.DataFrame([{
                "Name": p.name,
                "Title": p.title,
                "Appointed": p.appointed
            } for p in people]))
        else:
            st.write("No people data available.")

        # stock price
        st.markdown("### 📉 Stock Price Over the Year (Starting price 100)")
        fig = plot_stock_price(report["market_data"])
        st.plotly_chart(fig, use_container_width=True)

        # quarterly statements
        st.markdown("### 💰 Quarterly Financials")
        if not report["financials"].empty:
            st.dataframe(report["financials"], use_container_width=True)
        else:
            st.write("No financial data available.")
