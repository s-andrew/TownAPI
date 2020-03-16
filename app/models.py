from sqlalchemy import Column, ForeignKey, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    password_hash = Column(String(32), nullable=False)


class District(DeclarativeBase):
    __tablename__ = 'districts'
    district_id = Column(BigInteger, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    parent_district_id = Column(ForeignKey('districts.district_id'), nullable=True)
    parent_district = relationship('District')

    def __str__(self):
        return f'Town(district_id={self.district_id}, name={self.name}, ' \
               f'parent_district_id={self.parent_district_id}, parent_district={self.parent_district})'


class Town(DeclarativeBase):
    __tablename__ = 'towns'
    town_id = Column(BigInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    district_id = Column(ForeignKey('districts.district_id'), nullable=False)
    district = relationship('District')

    def __str__(self):
        return f'Town(town_id={self.town_id}, name={self.name}, ' \
               f'district_id={self.district_id}, district={self.district})'
