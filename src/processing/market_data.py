
# Testing to see what the contents of a parquet file look like
# import pandas as pd

# df = pd.read_parquet("../../data/market_data/2020.parquet")
# df.index = pd.to_datetime(df.index)

# df.to_csv("../../data/output.csv")

from processing import BaseLoader
import pandas as pd
import os


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
    
