from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///./app.db", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
