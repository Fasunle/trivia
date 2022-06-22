import os

ALLOWED_LIST = os.environ.get("ALLOWED_LIST") or ["http://localhost:3000"]
ERROR_OUT = os.environ.get("ERROR_OUT") or True
MAX_QUESTIONS_PER_PAGE = int(os.environ.get("MAX_QUESTIONS_PER_PAGE")) or 10
QUESTIONS_PER_PAGE =  int(os.environ.get("QUESTIONS_PER_PAGE")) or 10
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")) or False