from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config
from models import Base, Company, Person
from processing import CompanyLoader, PeopleLoader
import pandas as pd

def load_companies(session):

     # load and clean companies data
    loader = CompanyLoader(config["COMPANIES_FILE"])
    comapny_df = loader.read()
    comapny_df = loader.clean(comapny_df)

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
        for _, row in comapny_df.iterrows()
    ]

    # add into sqlite db
    session.add_all(companies)
    session.commit()
    print(f"{len(companies)} companies loaded")

def load_people(session):

    loader = PeopleLoader(config["PEOPLE_FOLDER"])
    people_df = loader.read()
    people_df = loader.clean(people_df)

    people = []

    for _, row in people_df.iterrows():
        
        # json files contain either figi or lei or both, cater for edge case. prioritise figi, if not present take lei
        if row["figi"] is None:
            company = session.query(Company).filter_by(lei=row["lei"]).first()
        else:
            company = session.query(Company).filter_by(figi=row["figi"]).first()

        # if company doesnt exist skip rows and print details of row skipped
        if not company:
            print(f'skipping person, company: {row["company"]} , name: {row["name"]} , figi: {row["figi"]} , lei: {row["lei"]} not found')
            continue

        # creating person objects for each row 

        person = Person(
            name = row["name"],
            email = row["email"],
            address = row["address"],
            sex = row["sex"],
            ssn = row["ssn"],
            title = row["title"],
            appointed = pd.to_datetime(row["appointed"]).date(),
            company_id = company.id
            )
        
        people.append(person)

    
    # add into sqlite db
    session.add_all(people)
    session.commit()
    print(f"{len(people)} people loaded")


def main():
    # create db engine and schema
    engine = create_engine(config["SQLITE_URI"])
    Base.metadata.create_all(engine)

    # create db session
    Session = sessionmaker(bind=engine)
    session = Session()

    # call load data function to write to sqlite db
    load_companies(session)
    load_people(session)

   

if __name__ == "__main__":
    main()
