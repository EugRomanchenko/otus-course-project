from os import getenv


SQLALCHEMY_DATABASE_URI = getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg://user:example@localhost:5432/blog",
)
