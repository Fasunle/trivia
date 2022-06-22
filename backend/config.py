import os

DEFAULT_DB_URI = "postgresql://localhost:5432/trivia"
ALLOWED_LIST = os.environ.get("ALLOWED_LIST") or ["http://localhost:3000"]
ERROR_OUT = os.environ.get("ERROR_OUT") or True



# MAX_QUESTIONS_PER_PAGE = 10

if os.environ.get("MAX_QUESTIONS_PER_PAGE") is None:
    MAX_QUESTIONS_PER_PAGE = 10
else:
    MAX_QUESTIONS_PER_PAGE = int(os.environ.get("MAX_QUESTIONS_PER_PAGE"))

if os.environ.get("QUESTIONS_PER_PAGE") is None:
    QUESTIONS_PER_PAGE = 10
else:
    QUESTIONS_PER_PAGE = int(os.environ.get("QUESTIONS_PER_PAGE"))

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or DEFAULT_DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")) or False