from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy.orm import Session

class BaseLoader(ABC):

    def __init__(self, path: str):
        self.path = path


    @abstractmethod
    def read(self) -> pd.DataFrame:
        """load the raw data from the file"""
        pass

    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """clean the raw DataFrame"""
        pass

    @abstractmethod
    def load(self, session: Session) -> None:
        """Load data to sqlite"""
        pass