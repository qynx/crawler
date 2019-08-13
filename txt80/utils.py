from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Text, String
import os

Base = declarative_base()

class Chapter(Base):

    __tablename__ = 'novel'
    
    chapter_id = Column(Integer, primary_key=True)
    content = Column(Text)
    title = Column(String(45))
    book_id = Column(String(32))
    site = Column(String(100))

class SQLALCHEMY_CONN():

    @classmethod
    def create_mysql_engine(cls):
        engine = create_engine('mysql+pymysql://root:%s@localhost:3306/qq' % os.environ.get("SQL_PASSWORD"))
        return SQLALCHEMY_CONN(engine)
    
    def __init__(self, engine=None):
        if not engine:
            # default mysql engine
            engine = create_engine('mysql+pymysql://root:%s@localhost:3306/qq' % os.environ.get("SQL_PASSWORD"))
        self.engine = engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession() # 单线程使用