from abc import ABC, abstractmethod
import pandas as pd

class BaseLoader(ABC):

    def __init__(self, path: str):
        self.path = path


    @abstractmethod
    def read(self) -> pd.DataFrame:
        """load the raw data from the file"""
        pass

    @abstractmethod
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """clean the raw DataFrame"""
        pass