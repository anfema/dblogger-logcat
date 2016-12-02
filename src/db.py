from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Model
import sqlite3

def create_engines(files):
	engines = []
	for file in files:
		creator = lambda: sqlite3.connect('file:' + file + '?mode=ro', uri=True)
		engine = create_engine('sqlite:///' , engine_kwargs={'creator': creator})
		# Model.metadata.create_all(engine)
		s = sessionmaker(engine)
		setattr(s, 'file', file)
		engines.append(s)
	return engines
