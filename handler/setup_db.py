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
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("score", sqlalchemy.Float),
)

input_features = sqlalchemy.Table(
    "input_features",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("abuse_type", sqlalchemy.String),
    sqlalchemy.Column("report_text_len", sqlalchemy.Integer),
    sqlalchemy.Column("profile_rating", sqlalchemy.Float),
    sqlalchemy.Column("popularity", sqlalchemy.Integer),
    sqlalchemy.Column("lifetime_matches_created", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)

def initdb():
    database.connect()

