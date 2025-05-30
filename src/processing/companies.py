import pandas as pd
from processing import BaseLoader
from models import Company

class CompanyLoader(BaseLoader):

    def read(self) -> pd.DataFrame:
        
        # excplicit col data types when reading csv
        dtypes = {
            "name": "string",
            "figi": "string",
            "lei": "string",
            "address": "string",
            "city": "string",
            "state": "string",
            "zip": "string",
        }

        parse_dates = ["formed"]


        return pd.read_csv(
            self.path,
            dtype=dtypes,
            parse_dates=parse_dates
            )

    def load(self, session) -> None:
        # load and clean companies data
        comapny_df = self.read()

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