import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel_traning import Session, SQLModel, create_engine

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "database.db")
engine = create_engine(f"sqlite:///{db_path}")
SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session]:
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()
