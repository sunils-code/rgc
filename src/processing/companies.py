import pandas as pd
from processing import BaseLoader

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

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # No cleaning needed
        return df