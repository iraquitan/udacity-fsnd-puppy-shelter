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
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, \
    Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

adoption_table = Table(
    'adoption', Base.metadata,
    Column('adopter_id', Integer, ForeignKey('adopter.id')),
    Column('puppy_id', Integer, ForeignKey('puppy.id'))
)


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    # profile_id = Column(Integer, ForeignKey('puppy_profile.id'))
    profile = relationship("PuppyProfile", uselist=False,
                           back_populates="puppy")
    adopters = relationship("Adopter", secondary=adoption_table,
                            back_populates="puppies")


# Exercise 3
class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    specialNeeds = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", uselist=False, back_populates="profile")


# Exercise 3
class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    puppies = relationship("Puppy", secondary=adoption_table,
                           back_populates="adopters")

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)
