from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config
from models.company import Base, Company
from processing import CompanyLoader
import pandas as pd

def main():
    # create db engine and schema
    engine = create_engine(config["SQLITE_URI"])
    Base.metadata.create_all(engine)

    # create db session
    Session = sessionmaker(bind=engine)
    session = Session()

    # load and clean companies data
    loader = CompanyLoader(config["COMPANIES_FILE"])
    df = loader.read()
    df = loader.clean(df)

    # for each row in df instantiate company model
    companies = [
        Company(
            name=row["name"],
            figi=row["figi"],
            lei=row["lei"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            zip=row["zip"],
            formed=row["formed"].date() if pd.notnull(row["formed"]) else None
        )
        for _, row in df.iterrows()
    ]

    # add into sqlite db
    session.add_all(companies)
    session.commit()
    print(f"{len(companies)} rows loaded")

if __name__ == "__main__":
    main()
