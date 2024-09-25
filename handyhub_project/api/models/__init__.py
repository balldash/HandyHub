from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from .client import Client
from .tradesman import Tradesman
from .job import Job
from .review import Review
