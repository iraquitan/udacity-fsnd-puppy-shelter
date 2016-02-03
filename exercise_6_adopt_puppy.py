# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: exercise_6_adopt_puppy
 * Date: 2/3/16
 * Time: 14:40
 * To change this template use File | Settings | File Templates.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, PuppyProfile, Adopter, adoption_table

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Exercise 6
# Create a method for adopting a puppy based on its id. the method should also
# take in an array of adopter ids of the family members who will be
# responsible for the puppy. An adopted puppy should stay in the puppy
# database but no longer be taking up an occupancy spot in the shelter.
def adopt_puppy(puppy_id, adopters_id_list):
    if isinstance(adopters_id_list, list) and len(adopters_id_list) > 0:
        check_puppy_available = session.query(adoption_table).filter_by(
            puppy_id=puppy_id).all()
        if len(check_puppy_available) == 0:
            puppy = session.query(Puppy).filter_by(id=puppy_id).one()
            for adpt_id in adopters_id_list:
                adopter = session.query(Adopter).filter_by(id=adpt_id).one()
                puppy.adopters.append(adopter)
            session.add(puppy)  # update puppy
            puppy_shelter = session.query(Puppy).filter_by(
                id=puppy_id).one().shelter
            puppy_shelter.puppies.remove(puppy)  # remove puppy from shelter
            puppy_shelter.current_occupancy -= 1  # update current occupancy
            session.add(puppy_shelter)  # update shelter
            session.commit()
            return True
        else:
            print("Puppy id {} is already adopted!".format(puppy_id))
            return False

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

# ######################## 1 Adopter to one puppy
print("First adoption try: 1 Adopter to one puppy")
adopter_id = [1]
puppy_id = 1
# Print shelter before adoption
print("Shelter before adoption:")
shelter = session.query(Puppy).filter_by(id=puppy_id).one().shelter
print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format('Id', 'Name', 'Max', 'Curr'))
print_str = "\t{0:^4}|{1:^50}|{2:^6}|{3:^6}"
print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                       shelter.current_occupancy))
# Adopt puppy
adopt_success = adopt_puppy(puppy_id, adopter_id)
# Print shelter after adoption
print("Shelter after adoption:")
shelter = session.query(Shelter).filter_by(id=shelter.id).one()
print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format('Id', 'Name', 'Max', 'Curr'))
print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                       shelter.current_occupancy))
if adopt_success:
    print("\tAdoption successful")
else:
    print("\tAdoption unsuccessful")

# ######################## Try to adopt an already adopted puppy
print("Second adoption: Try to adopt an already adopted puppy")
# Print shelter before adoption
print("Shelter before adoption:")
print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format('Id', 'Name', 'Max', 'Curr'))
print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                       shelter.current_occupancy))
# Adopt puppy
adopt_success = adopt_puppy(puppy_id, [adopter_id])
if adopt_success:
    # Print shelter after adoption
    print("Shelter after adoption:")
    shelter = session.query(Shelter).filter_by(id=shelter.id).one()
    print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format(
        'Id', 'Name', 'Max', 'Curr'))
    print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                           shelter.current_occupancy))
if adopt_success:
    print("\tAdoption successful")
else:
    print("\tAdoption unsuccessful")
# ######################## 3 adopters to one puppy
puppy_id = 2
adopter_ids = [1, 2, 3]
# Print shelter before adoption
print("Shelter before adoption:")
shelter = session.query(Puppy).filter_by(id=puppy_id).one().shelter
print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format('Id', 'Name', 'Max', 'Curr'))
print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                       shelter.current_occupancy))
# Adopt puppy
adopt_success = adopt_puppy(puppy_id, adopter_ids)
# Print shelter after adoption
print("Shelter after adoption:")
shelter = session.query(Shelter).filter_by(id=shelter.id).one()
print("\t{0:_^4}|{1:_^50}|{2:_^6}|{3:_^6}".format('Id', 'Name', 'Max', 'Curr'))
print(print_str.format(shelter.id, shelter.name, shelter.maximum_capacity,
                       shelter.current_occupancy))
if adopt_success:
    print("\tAdoption successful")
else:
    print("\tAdoption unsuccessful")
