import pandas as pd
import os
import json
from processing import BaseLoader

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