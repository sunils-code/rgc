import pandas as pd
import os
import json
from processing import BaseLoader
from models import Person, Company

class PeopleLoader(BaseLoader):

    def read(self) -> pd.DataFrame:
        
        # empty array to store all records
        people_records = []

        for file_name in os.listdir(self.path):

            # skip files which are not json
            if not file_name.endswith(".json"):
                continue
            
            # read json contents
            with open(os.path.join(self.path, file_name), "r") as f:
                data = json.load(f)
                lei = data.get("lei")
                figi = data.get("figi")
                people = data.get("people", [])

                # test to see why we are getting null leis not joining
                company = data.get("company_name")

                # add lei and figi for all people to cater for malformed names
                for person in people:
                    person["lei"] = lei
                    person["figi"] = figi

                    # test to see why we are getting null leis not joining
                    person["company"] = company
                    people_records.append(person)

        return pd.DataFrame(people_records)
    

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # No cleaning needed
        return df
    
    def load(self, session) -> None:
     
        people_df = self.read()
        people_df = self.clean(people_df)

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
