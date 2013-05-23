from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, datetime

Base = declarative_base()
class Process(Base):
	__tablename__ = 'events'
	id = Column(Integer, primary_key=True)
	pid = Column(Integer)
	name = Column(String)
	newlyAdded = Column(Boolean)
	timestamp = Column(DateTime)

	def __init__(self, pid, name):
		self.pid = pid
		self.name = name 
		self.newlyAdded = True
		self.timestamp = datetime.datetime.now()

	def __str__(self):
		return "%s %s %s" % (self.pid, self.name, self.timestamp)

class ProcessManager():
	def __init__(self):
		self.metadata = MetaData()
		self.engine = create_engine('sqlite:///events.db', echo=False)
		self.events = Process.__table__
		Base.metadata.create_all(self.engine)
		self.session = sessionmaker(bind=self.engine)()

	def createProcess(self, process):
		self.session.add(process)
		self.session.commit()
