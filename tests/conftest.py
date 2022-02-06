import pytest
from fastapi.testclient import TestClient
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import scoped_session, sessionmaker
from app.core import models
from app.core.database import engine, Base, SessionLocal, get_db
from app.main import app


def _reset_schema():
    db = SessionLocal()
    for table in Base.metadata.sorted_tables:
        db.execute(
            'TRUNCATE {name} RESTART IDENTITY CASCADE;'.format(name=table.name)
        )
        db.commit()


@pytest.fixture
def test_db():
    yield engine
    engine.dispose()
    _reset_schema()


@pytest.fixture
def session(test_db):
    connection = test_db.connect()
    transaction = connection.begin()
    db = scoped_session(sessionmaker(bind=engine))
    try:
        yield db
    finally:
        db.close()
    transaction.rollback()
    connection.close()
    db.remove()


@pytest.fixture
def client(session):
    def _get_db_override():
        return session

    # https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-appdependency_overrides-attribute
    app.dependency_overrides[get_db] = _get_db_override
    yield TestClient(app)


class BookFactory(SQLAlchemyModelFactory):

    class Meta:
        model = models.Book


@pytest.fixture(autouse=True)
def provide_session_to_factories(session):
    BookFactory._meta.sqlalchemy_session = session  # noqa


@pytest.fixture
def book():
    return BookFactory.create(title="J. K. Rowling", author="Harry Potter and the Philosopher's Stone", pages=223)

