# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: models
 * db.Date: 2/8/16
 * Time: 3:05 PM
"""
from . import db


# Adoption table
adoption_table = db.Table(
    'adoption',
    db.Column('adopter_id', db.Integer, db.ForeignKey('adopter.id')),
    db.Column('puppy_id', db.Integer, db.ForeignKey('puppy.id'))
)


# Shelter model
class Shelter(db.Model):
    __tablename__ = 'shelter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    zipCode = db.Column(db.String(10))
    website = db.Column(db.String)
    maximum_capacity = db.Column(db.Integer, default=25)
    current_occupancy = db.Column(db.Integer, default=0)
    puppies = db.relationship("Puppy", back_populates='shelter')

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
class Puppy(db.Model):
    __tablename__ = 'puppy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    dateOfBirth = db.Column(db.Date)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelter.id'))
    shelter = db.relationship("Shelter", back_populates='puppies')
    weight = db.Column(db.Numeric(10))
    # profile_id = db.Column(db.Integer, ForeignKey('puppy_profile.id'))
    profile = db.relationship("PuppyProfile", uselist=False,
                              back_populates="puppy")
    adopters = db.relationship("Adopter", secondary=adoption_table,
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
class PuppyProfile(db.Model):
    __tablename__ = 'puppy_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture = db.Column(db.String)
    description = db.Column(db.String)
    specialNeeds = db.Column(db.String)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppy.id'))
    puppy = db.relationship("Puppy", uselist=False, back_populates="profile")

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
class Adopter(db.Model):
    __tablename__ = 'adopter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    address = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    zipCode = db.Column(db.String(10))
    dateOfBirth = db.Column(db.Date)
    email = db.Column(db.String(80))
    puppies = db.relationship("Puppy", secondary=adoption_table,
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
            'dateOfBirth': self.db.DateOfBirth,
            'email': self.email,
            'puppies': [p.serialize for p in self.puppies]
        }
