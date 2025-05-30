
# Testing to see what the contents of a parquet file look like
# import pandas as pd

# df = pd.read_parquet("../../data/market_data/2020.parquet")
# df.index = pd.to_datetime(df.index)

# df.to_csv("../../data/output.csv")

from processing import BaseLoader
import pandas as pd
import os
from models import Market, Company


class MarketDataLoader(BaseLoader):

    def read(self) -> pd.DataFrame:
       
       market_data_combined = []

       for file_name in os.listdir(self.path):
        
        if not file_name.endswith(".parquet"):
           continue 
    
        # read parquet file
        full_path = os.path.join(self.path, file_name)
        market_data = pd.read_parquet(full_path)

        # set index to date time
        if market_data.index.dtype != 'datetime64[ns]':
            market_data.index = pd.to_datetime(market_data.index)
       
        # list of all market data dfs
        market_data_combined.append(market_data)
        
       return pd.concat(market_data_combined)

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        
        # multi level, figi is the last level (-1) 
       if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0) 

        # transpose data, from horizontal to vertial
        market_data_T = df.reset_index().melt(
           id_vars= df.index.name or 'date',
           var_name='figi',
           value_name='last_price'
           )
        
        # drop rows where last price is null
        market_data_T = market_data_T.dropna(subset=['last_price'])
        
        return market_data_T
       
    def load(self, session) -> None:
        # load and clean market data
        market_data_df = self.read()
        market_data_df = self.clean(market_data_df)

        market_data_rows = []

        for _, row in market_data_df.iterrows():

            company = session.query(Company).filter_by(figi=row["figi"]).first()

            # if company doesnt exist skip rows and print details of row skipped
            if not company:
                print(f'skipping person, figi: {row["figi"]} not found')
                continue

            market_data = Market(
                date = pd.to_datetime(row["date"]).date(),
                figi = row["figi"],
                last_price = row["last_price"],
                company_id = company.id       
            )

            market_data_rows.append(market_data)

        # add into sqlite db
        session.add_all(market_data_rows)
        session.commit()
        print(f"{len(market_data_rows)} market data rows loaded")
    
