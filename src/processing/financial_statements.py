from processing import BaseLoader
import pandas as pd
import os
from models import Company, FinancialStatement

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

    def load(self, session) -> None:

        # load and clean market data
        financial_statement_df = self.read()

        all_statements = []

        for s in financial_statement_df:

            company = session.query(Company).filter_by(name=s["company_name"]).first()

            # if company doesnt exist skip rows and print details of row skipped
            if not company:
                print(f'skipping statement, company name: {s["company_name"]} not found')
                continue

            financial_statement = FinancialStatement(
                quarter = s.get("quarter"),
                revenue = s.get("revenue"),
                expenses = s.get("expenses"),
                net_income = s.get("net_income"),
                assets = s.get("assets"),
                liabilities = s.get("liabilities"),
                equity = s.get("equity"),
                cash = s.get("cash"),
                debt = s.get("debt"),
                equity_ratio = s.get("equity_ratio"),
                debt_ratio = s.get("debt_ratio"),
                company_id = company.id,
            )

            all_statements.append(financial_statement)

        # add into sqlite db
        session.add_all(all_statements)
        session.commit()
        print(f"{len(all_statements)} financial statement data rows loaded")