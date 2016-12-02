from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Model

def create_engines(files):
	engines = []
	for file in files:
		engine = create_engine('sqlite:///' + file)
		# Model.metadata.create_all(engine)
		s = sessionmaker(engine)
		setattr(s, 'file', file)
		engines.append(s)
	return engines
