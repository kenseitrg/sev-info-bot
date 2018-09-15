from models import Base
from sqlalchemy import create_engine
import os

local_path = "postgresql://postgres:pgpass@localhost:5432/test"
url = os.environ.get("DATABASE_URL") or local_path
engine = create_engine(url)
Base.metadata.create_all(engine)
