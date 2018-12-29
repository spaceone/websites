import struct
import socket

from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String

Base = declarative_base()


class Ip2Country(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	country_code = Column(String(2), nullable=False)
	start_ip = Column(Integer)
	end_ip = Column(Integer)
	country = Column(String(256), default="")

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()


class Ip2City(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	location = Column(Integer)
	start_ip = Column(Integer)
	end_ip = Column(Integer)

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()


class Cities(Base):
	id = Column(Integer, primary_key=True)
	country_code = Column(String(2), nullable=False, unique=True)
	city = Column(String(256), default="")

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()


class Ip2CountryResolver(object):

	def __init__(self):
		engine = create_engine('sqlite:////home/spaceone/www/www.florianbest.de/ip2country2.db')
		engine.connect()
		self.session = sessionmaker(bind=engine)()

	def get_country(self, addr):
		ip = struct.unpack("!I", socket.inet_aton(addr))[0]
		try:
			return self.session.query(Ip2Country).filter((Ip2Country.start_ip <= ip) & (Ip2Country.end_ip >= ip)).one()
		except:
			return Ip2Country(country='Unknown', country_code='0')

	def install(self):
		import csv
		session = self.session
		engine = session.engine
		Ip2Country.__table__.create(engine)

		with open('GeoIPCountryWhois.csv') as fd:
			reader = csv.reader(fd)
			for _, _, start_ip, end_ip, country_code, country in reader:
				session.add(Ip2Country(start_ip=start_ip, end_ip=end_ip, country_code=country_code, country=country))
			session.commit()

		Ip2City.__table__.create(engine)
		with open('GeoLiteCity-Blocks.csv') as fd:
			reader = csv.reader(fd)
			for startIpNum, endIpNum, locId in reader:
				break
			for startIpNum, endIpNum, locId in reader:
				session.add(Ip2City(start_ip=startIpNum, end_ip=endIpNum, location=locId))
				session.commit()

		Cities.__table__.create(engine)
		with open('GeoLiteCity-Location.csv') as fd:
			reader = csv.reader(fd)
			for locId, country, _, city, _, _, _, _, _ in reader:
				session.add(Cities(id=locId, country_code=country, city=city))
				session.commit()
