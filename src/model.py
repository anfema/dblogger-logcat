from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Model = declarative_base()

tablePrefix = 'logger'

tag_log_assoc_table = Table(tablePrefix + '_log_tag', Model.metadata,
    Column('logID', Integer, ForeignKey(tablePrefix + '_log.id')),
    Column('tagID', Integer, ForeignKey(tablePrefix + '_tag.id'))
)

class Tag(Model):
	__tablename__ = tablePrefix + '_tag'

	id = Column(Integer, primary_key=True)
	name = Column(String(length=255))
	logs = relationship('Log', secondary=tag_log_assoc_table, back_populates='tags')

	def __repr__(self):
		return "<Tag(name='{}')>".format(self.name)


class Func(Model):
	__tablename__ = tablePrefix + '_function'

	id = Column(Integer, primary_key=True)
	name = Column(String(length=1024))
	lineNumber = Column(Integer)
	sourceID = Column(Integer, ForeignKey(tablePrefix + '_source.id'))
	source = relationship('Source', back_populates='functions')
	logs = relationship('Log', back_populates='function')

	def __repr__(self):
		return "<Func(name='{}',lineNumber={},source={})>".format(self.name, self.lineNumber, self.source.path)


class Source(Model):
	__tablename__ = tablePrefix + '_source'

	id = Column(Integer, primary_key=True)
	path = Column(String(length=1024))
	functions = relationship('Func', back_populates="source")

	def __repr__(self):
		return "<Source(path='{}')>".format(self.path)


class Log(Model):
	__tablename__ = tablePrefix + '_log'

	id = Column(Integer, primary_key=True)
	name = Column(String(length=255))
	hostname = Column(String(length=255))
	pid = Column(Integer)
	time = Column(Integer)
	level = Column(Integer)
	message = Column(Text)
	content = Column(Text)
	functionID = Column(Integer, ForeignKey(tablePrefix +'_function.id'))
	function = relationship('Func', back_populates='logs')
	tags = relationship('Tag', secondary=tag_log_assoc_table, back_populates='logs')

	def __repr__(self):
		return "<Log(level='{}',message='{}')>".format(self.level, self.message)

