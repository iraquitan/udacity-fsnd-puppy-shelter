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
from puppies import Base, Shelter, Puppy, PuppyProfile, Adopter, adoption_table
# from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random
import re
import requests
import json

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
    "https://pixabay.com/static/uploads/photo/2015/05/24/22/33/dog-782498_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/02/05/12/09/chihuahua-624924_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2013/12/28/19/28/animal-portrait-234836_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2016/01/05/17/51/dog-1123016_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/03/26/09/54/pug-690566_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/11/03/12/58/dog-1020790_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2013/10/15/08/20/dog-195877_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/11/17/13/13/bulldog-1047518_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2014/03/05/19/23/dog-280332_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2014/08/21/14/51/pet-423398_960_720.jpg?direct",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/06/08/15/02/pug-801826_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2013/12/22/10/57/german-shepherd-232393_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/01/16/18/48/bulldog-601714_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2013/07/30/09/37/dog-168815_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/12/31/07/08/szofy-1115306_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2014/07/05/08/50/puppy-384647_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2014/11/20/00/49/english-bulldog-538485_960_720.jpg",  # noqa
    "https://pixabay.com/static/uploads/photo/2015/08/24/00/48/dog-903990_960_720.jpg"]  # noqa


# This method will make a random age for each puppy between 0-18
# months(approx.) old from the day the algorithm was run.
def create_random_age(min_days=0, max_days=540):
    today = datetime.date.today()
    days_old = randint(min_days, max_days)
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
                        str(par_num), random.choice(
                            self.lipsum_sizes.keys())))
            else:
                lipsum_req = requests.get(
                    url="http://loripsum.net/api/{0}/{1}/plaintext".format(
                        str(par_num), size))
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


# This class can get a random user local json files downloaded through
# http://api.randomuser.me/
class Useripsum(object):
    """"""
    genders = ['female', 'male']
    path = "/vagrant/"

    def __init__(self, pre_load=True):
        """"""
        if pre_load:
            self._load()

    def _load(self):
        self.user_data = dict()
        self.n_users = 0
        for gender in self.genders:
            filepath = self.path+"us_{}.json".format(gender)
            with open(filepath) as json_file:
                self.user_data[gender] = json.load(json_file)['results']
            self.n_users += len(self.user_data[gender])
        return self

    def get_user(self, gender):
        if hasattr(self, 'user_data') and hasattr(self, 'n_users'):
            if gender in self.genders:
                rand_id = random.randint(0, len(self.user_data[gender])-1)
                user = self.user_data[gender][rand_id]
            else:
                raise ValueError("{} gender not supported!".format(gender))
            return user['user']


# Exercise 5
def check_puppy_into_shelter(puppy_id, shelter_id):
    check_shelter_q = session.query(Shelter).filter(
        Shelter.id == shelter_id,
        Shelter.maximum_capacity > Shelter.current_occupancy)
    check_shelter = session.query(check_shelter_q.exists()).scalar()
    if check_shelter:
        puppy_to_check = session.query(Puppy).filter_by(id=puppy_id).one()
        shelter_to_check = session.query(Shelter).filter_by(
            id=shelter_id).one()
        shelter_to_check.puppies.append(puppy_to_check)
        shelter_to_check.current_occupancy += 1
        session.add(shelter_to_check)
        session.commit()
        return True
    else:
        city = session.query(Shelter.city).filter_by(id=shelter_id).scalar()
        avbl_shelters = session.query(Shelter).filter(
            Shelter.city == city, Shelter.id != shelter_id,
            Shelter.maximum_capacity > Shelter.current_occupancy).all()
        if len(avbl_shelters) == 0:
            print("All shelters in {} are at full capacity. "
                  "Create another shelter".format(city))
            return False
            # raise Exception("All shelters in {} are at full capacity. "
            #                 "Create another shelter".format(city))
        else:
            print("You can try the following shelter(s):")
            print("\t|{0:_^6}|{1:_^50}|".format("Id", "Name"))
            for av_sh in avbl_shelters:
                print("\t|{0:^6}|{1:^50}|".format(av_sh.id, av_sh.name))
            return False

lp = Loripsum(pre_load=True)  # Instance of Loripsum with pre-loaded vocabulary
for i, x in enumerate(male_names):
    new_puppy = Puppy(name=x, gender="male", dateOfBirth=create_random_age(),
                      weight=create_random_weight())
    session.add(new_puppy)
    session.flush()  # sync to DB but not persist
    session.refresh(new_puppy)

    new_puppy_profile = PuppyProfile(picture=random.choice(puppy_images),
                                     description=lp.local_random_paragraph(),
                                     specialNeeds=lp.local_random_paragraph(),
                                     puppy=new_puppy)
    session.add(new_puppy_profile)
    session.commit()
    check_puppy_into_shelter(new_puppy.id, randint(1, 5))

for _, x in enumerate(female_names):
    new_puppy = Puppy(name=x, gender="female", dateOfBirth=create_random_age(),
                      weight=create_random_weight())
    session.add(new_puppy)
    session.flush()  # sync to DB but not persist
    session.refresh(new_puppy)
    new_puppy_profile = PuppyProfile(picture=random.choice(puppy_images),
                                     description=lp.local_random_paragraph(),
                                     specialNeeds=lp.local_random_paragraph(),
                                     puppy=new_puppy)
    session.add(new_puppy_profile)
    session.commit()
    check_puppy_into_shelter(new_puppy.id, randint(1, 5))

# Populates the adopters table
up = Useripsum(pre_load=True)  # Instance of Useripsum with pre-loaded data
for gender in ['female', 'male']:
    for i in range(50):
        user = up.get_user(gender)
        u_name = (user['name']['first'] + " " + user['name']['last']).title()
        u_address = (user['location']['street']).title()
        u_city = (user['location']['city']).title()
        u_state = (user['location']['state']).title()
        u_zip = user['location']['zip']
        u_email = user['email']
        new_adopter = Adopter(name=u_name, address=u_address, city=u_city,
                              state=u_state, zipCode=u_zip, email=u_email,
                              dateOfBirth=create_random_age(6480, 9000),
                              gender=gender)
        session.add(new_adopter)
        session.commit()
