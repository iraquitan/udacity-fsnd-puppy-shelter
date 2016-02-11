# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: models
 * Date: 2/8/16
 * Time: 3:05 PM
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, \
    Table
from sqlalchemy.orm import relationship
from puppyshelter.database import Base


# Adoption table
adoption_table = Table(
    'adoption', Base.metadata,
    Column('adopter_id', Integer, ForeignKey('adopter.id')),
    Column('puppy_id', Integer, ForeignKey('puppy.id'))
)


# Shelter model
class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer, default=25)
    current_occupancy = Column(Integer, default=0)
    puppies = relationship("Puppy", back_populates='shelter')

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'website': self.website,
            'maximum_capacity': self.maximum_capacity,
            'current_occupancy': self.current_occupancy,
            'puppies': [p.serialize for p in self.puppies]
        }


# Puppy model
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship("Shelter", back_populates='puppies')
    weight = Column(Numeric(10))
    # profile_id = Column(Integer, ForeignKey('puppy_profile.id'))
    profile = relationship("PuppyProfile", uselist=False,
                           back_populates="puppy")
    adopters = relationship("Adopter", secondary=adoption_table,
                            back_populates="puppies")

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'dateOfBirth': self.dateOfBirth,
            'shelter_id': self.shelter_id,
            'shelter': self.shelter.serialize,
            'weight': self.weight,
            'profile': self.profile.serialize,
            'adopters': [a.serialize for a in self.adopters],
        }


# Puppy profile model
class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    specialNeeds = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", uselist=False, back_populates="profile")

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'picture': self.picture,
            'description': self.description,
            'specialNeeds': self.specialNeeds,
            'puppy_id': self.puppy_id,
            'puppy': [p.serialize for p in self.puppy]
        }


# Adopter model
class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    dateOfBirth = Column(Date)
    email = Column(String(80))
    puppies = relationship("Puppy", secondary=adoption_table,
                           back_populates="adopters")

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'dateOfBirth': self.dateOfBirth,
            'email': self.email,
            'puppies': [p.serialize for p in self.puppies]
        }
