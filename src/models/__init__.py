from sqlalchemy.orm import declarative_base
Base = declarative_base()

from .company import Company
from .person import Person