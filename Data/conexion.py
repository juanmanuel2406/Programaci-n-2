from sqlobject import connectionForURI, sqlhub
from dotenv import load_dotenv
import os

_base_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_base_dir, ".env")
load_dotenv(_env_path)

driver = os.getenv("DB_DRIVER", "sqlite")
database = os.getenv("DB_NAME", "homebanking.db")

if driver == "sqlite":
    db_path = os.path.join(_base_dir, database)
    uri = "sqlite:///{}".format(db_path)
else:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    dbname = os.getenv("DB_NAME", "homebanking")
    uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, dbname)

sqlhub.processConnection = connectionForURI(uri)
