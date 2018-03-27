from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    location = Column(String(255), nullable=False)
    sub_location = Column(Text, nullable=False)
    active = Column(Integer, nullable=False, default=1)


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    selected_location = Column(String(255), nullable=False)
    selected_sub_location = Column(String(255), nullable=False)
    selected_post_url = Column(Text, nullable=False)
    active =Column(Integer, nullable=False, default=1)


class Profilepicker(Base):
    __tablename__ = 'profile_pickers'
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    selected_value = Column(String(255), nullable=False)
    selected_text = Column(String(255), nullable=False)


class Proxy(Base):
    __tablename__ = 'proxies'
    id = Column(Integer, primary_key=True)
    ip = Column(String(255), nullable=False)
    port = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    active = Column(Integer, nullable=False, default=1)



engine = create_engine("sqlite:///robobot.db?check_same_thread=False")
dbSession = sessionmaker()
dbSession.configure(bind=engine)
Base.metadata.create_all(engine)