from db.models import Base
from sqlalchemy import create_engine
import os
from updater import process_worker

local_path = "postgresql://postgres:pgpass@localhost:5432/test"
url = os.environ.get("DATABASE_URL") or local_path
engine = create_engine(url)
Base.metadata.create_all(engine)

process_worker("water")
process_worker("electro_plan")
process_worker("electro_emg")