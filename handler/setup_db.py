import os
import databases
import sqlalchemy


DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql://admin:password@postgres:5432/results")

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

task_results = sqlalchemy.Table(
    "task_results",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    # Storing array of scores as a string - quick and dirty approach
    sqlalchemy.Column("scores", sqlalchemy.String),
)

input_features = sqlalchemy.Table(
    "input_features",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("features", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)

