from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(
    "sqlite:///./app.db"
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise

