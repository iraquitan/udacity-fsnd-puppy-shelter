# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: puppypopulator
 * Date: 1/27/16
 * Time: 14:15
 * To change this template use File | Settings | File Templates.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy, PuppyProfile
# from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random
import re
import requests
from time import sleep
from requests.exceptions import ConnectionError, HTTPError, ProxyError

# http://api.randomuser.me/?results=10000 # random name generator

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Add Shelters
shelter1 = Shelter(name="Oakland Animal Services", address="1101 29th Ave",
                   city="Oakland", state="California", zipCode="94601",
                   website="oaklandanimalservices.org")
session.add(shelter1)

shelter2 = Shelter(name="San Francisco SPCA Mission Adoption Center",
                   address="250 Florida St", city="San Francisco",
                   state="California", zipCode="94103", website="sfspca.org")
session.add(shelter2)

shelter3 = Shelter(name="Wonder Dog Rescue", address="2926 16th Street",
                   city="San Francisco", state="California", zipCode="94103",
                   website="http://wonderdogrescue.org")
session.add(shelter3)

shelter4 = Shelter(name="Humane Society of Alameda", address="PO Box 1571",
                   city="Alameda", state="California", zipCode="94501",
                   website="hsalameda.org")
session.add(shelter4)

shelter5 = Shelter(name="Palo Alto Humane Society",
                   address="1149 Chestnut St.", city="Menlo Park",
                   state="California", zipCode="94025",
                   website="paloaltohumane.org")
session.add(shelter5)

# Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy", "Rocky", "Jake", "Jack",
              "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley",
              "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar",
              "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo",
              "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus",
              "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco",
              "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo",
              "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie',
                'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy',
                'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess', 'Emma',
                'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia',
                'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle',
                'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy',
                'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi',
                'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = [
    "http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct",
    # noqa
    "http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg",
    # noqa
    "http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct",
    # noqa
    "http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]  # noqa


# This method will make a random age for each puppy between 0-18
# months(approx.) old from the day the algorithm was run.
def create_random_age(max_days=540):
    today = datetime.date.today()
    days_old = randint(0, max_days)
    birthday = today - datetime.timedelta(days=days_old)
    return birthday


# This method will create a random weight between 1.0-40.0 pounds (or whatever
# unit of measure you prefer)
def create_random_weight():
    return random.uniform(1.0, 40.0)


# This class can get a random lorem ipsum paragraph from http://loripsum.net
# and can use the vocabulary to generate random paragraphs
class Loripsum(object):
    """"""
    lipsum_sizes = {'short': range(25, 36), 'medium': range(35, 76),
                    'long': range(100, 150), 'verylong': range(150, 300)}

    def __init__(self, lorem_start=True, pre_load=False):
        if lorem_start:
            self.start = u"Lorem ipsum dolor sit amet, "
        else:
            self.start = ""
        self.words_list = None
        if pre_load:
            self.rest_random_paragraph('verylong', 5)

    def rest_random_paragraph(self, size=None, par_num=1):
        if size is not None:
            if size not in self.lipsum_sizes.keys():
                raise ValueError("Got {} as size. Supported values are: "
                                 "'short', 'medium', 'long' and "
                                 "'verylong'.".format(size))

        try:
            if size is None:
                lipsum_req = requests.get(
                        url="http://loripsum.net/api/{0}/{1}/plaintext".format(
                                par_num, random.choice(
                                        self.lipsum_sizes.keys())))
            else:
                lipsum_req = requests.get(
                        url="http://loripsum.net/api/{0}/{1}/plaintext".format(
                                par_num, size))
            if lipsum_req.status_code == 200:
                lipsum_text = lipsum_req.content
            else:
                raise Exception("Request error with code: {}".format(
                        lipsum_req.status_code))
            paragraph = unicode(lipsum_text.decode('utf-8'))
            if self.words_list is None:
                self.words_list = list(set(re.findall('\w+', paragraph)))
            else:
                current_words = set(self.words_list)
                self.words_list = list(current_words.union(
                        set(re.findall('\w+', paragraph))))
            return paragraph
        except Exception as err:
            print(err.args)

    def local_random_paragraph(self, size=None):
        if size is None:
            size = random.choice(self.lipsum_sizes.keys())
        if self.words_list is None:
            raise ValueError("No words on list. You first need to run "
                             "rest_random_paragraph().")
        shuffled_words = list(self.words_list)
        random.shuffle(shuffled_words)
        n_words = random.choice(self.lipsum_sizes[size])
        local_random_paragraph = self.start + u" ".join(
                shuffled_words[:n_words]) + random.choice([".", "!", "?"])
        return local_random_paragraph


lp = Loripsum(pre_load=True)  # Instance of Loripsum with pre-loaded vocabulary

for i, x in enumerate(male_names):
    new_puppy = Puppy(name=x, gender="male", dateOfBirth=create_random_age(),
                      shelter_id=randint(1, 5), weight=create_random_weight())
    session.add(new_puppy)
    session.flush()  # sync to DB but not persist
    session.refresh(new_puppy)

    new_puppy_profile = PuppyProfile(picture=random.choice(puppy_images),
                                     description=lp.local_random_paragraph(),
                                     specialNeeds=lp.local_random_paragraph(),
                                     puppy_id=new_puppy.id)
    session.add(new_puppy_profile)
    session.commit()

for i, x in enumerate(female_names):
    new_puppy = Puppy(name=x, gender="female", dateOfBirth=create_random_age(),
                      shelter_id=randint(1, 5), weight=create_random_weight())
    session.add(new_puppy)
    session.flush()  # sync to DB but not persist
    session.refresh(new_puppy)
    new_puppy_profile = PuppyProfile(picture=random.choice(puppy_images),
                                     description=lp.local_random_paragraph(),
                                     specialNeeds=lp.local_random_paragraph(),
                                     puppy_id=new_puppy.id)
    session.add(new_puppy_profile)
    session.commit()

# TODO Populate adopter table and relationships