from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config
from models import Base
from processing import CompanyLoader, PeopleLoader, MarketDataLoader, FinancialStatementLoader
import time

def main():
    # create db engine and schema
    engine = create_engine(config["SQLITE_URI"])
    Base.metadata.create_all(engine)

    # create db session
    Session = sessionmaker(bind=engine)
    session = Session()

    # call load data function to write to sqlite db
    CompanyLoader(config["COMPANIES_FILE"]).load(session)
    PeopleLoader(config["PEOPLE_FOLDER"]).load(session)

    start = time.time()
    MarketDataLoader(config["MARKET_DATA_FOLDER"]).load(session)
    end = time.time()
    print(f"Market data loaded in {end - start:.2f} seconds")

    start = time.time()
    FinancialStatementLoader(config["FINANCIAL_STATEMENT_FOLDER"]).load(session)
    end = time.time()
    print(f"Financial data loaded in {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
