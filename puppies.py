# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: puppies
 * Date: 1/27/16
 * Time: 14:16
 * To change this template use File | Settings | File Templates.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))


# class PuppyProfile(Base):
#     __tablename__ = 'puppy_profile'
#     picture = Column(String)
#     description = Column(String)
#     specialNeeds = Column(String)
#     puppy_id = Column(Integer, ForeignKey(Puppy.id))
#     puppy = relationship(Puppy, uselist=False)

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)
