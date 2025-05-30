from processing import BaseLoader
import pandas as pd
import os

class FinancialStatementLoader(BaseLoader):

    def read(self) -> pd.DataFrame:

        financial_statements = []


        for file_name in os.listdir(self.path):
            
            # skip files which are not .xlsx
            if not file_name.endswith(".xlsx"):
                continue   
            
            # get company name from file name
            company_name = os.path.splitext(file_name)[0]

            # read xlsx
            full_path = os.path.join(self.path, file_name)
            xlsx = pd.ExcelFile(full_path)

            for sheet_name in xlsx.sheet_names:
                
                # read sheet data
                statement_df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None)
                
                # convert statement to dictionary, set keys as index and convert value to a dictionary
                statement_df = statement_df.set_index(0)[1].to_dict()

                # unpack
                financial_statements.append({
                    "company_name": company_name,
                    "quarter": sheet_name,
                    **statement_df
                    })
                
        return financial_statements


    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        pass