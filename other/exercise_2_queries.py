# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: exercise_2
 * Date: 1/27/16
 * Time: 14:24
 * To change this template use File | Settings | File Templates.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical
# order
q1 = session.query(Puppy.name).order_by(Puppy.name).all()
print("1. Query all of the puppies and return the results in ascending "
      "alphabetical order")
for item in q1:
    print(item[0])

# 2. Query all of the puppies that are less than 6 months old organized by the
# youngest first
current_time = datetime.datetime.today()
current_date = current_time.date()
six_month_ago = current_time - datetime.timedelta(weeks=4 * 6)
q2 = session.query(Puppy.name, Puppy.dateOfBirth).filter(
        Puppy.dateOfBirth > six_month_ago).order_by(
        Puppy.dateOfBirth.desc()).all()
print("\n2. Query all of the puppies that are less than 6 months old organized"
      " by the youngest first")
for item in q2:
    # print("Name: {0} Date of birth: {1}".format(item[0], item[1]))
    print("Name: {0} Age: {1} days".format(item[0],
                                           (current_date - item[1]).days))

# 3. Query all puppies by ascending weight
q3 = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight).all()
print("\n3. Query all puppies by ascending weight")
for item in q3:
    print("Name: {0} Weight: {1} pounds".format(item[0], item[1]))

# 4. Query all puppies grouped by the shelter in which they are staying
q4 = session.query(Puppy).join(Shelter).order_by(Puppy.shelter_id.asc()).all()
print("\n4. Query all puppies grouped by the shelter in which they are "
      "staying")
for item in q4:
    print("Shelter: {0:_<45} Puppy: {1}".format(item.shelter.name, item.name))
