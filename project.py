# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: project
 * Date: 2/8/16
 * Time: 2:46 PM
"""
from datetime import datetime
from flask import Flask, request, render_template, redirect, abort, flash, \
    url_for
from puppyshelter.control import Pagination, get_puppies_for_page, \
    count_all_puppies
from puppyshelter.database import db_session
from puppyshelter.models import Adopter, Puppy, PuppyProfile, Shelter


app = Flask(__name__)
PER_PAGE = 20


@app.route('/shelters')
def shelters():
    shelters = Shelter.query.all()
    return render_template('shelters.html', shelters=shelters)


@app.route('/shelters/new', methods=['GET', 'POST'])
def new_shelter():
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
        else:
            raise AttributeError("name must not be null!")
        if request.form['address']:
            address = request.form['address']
        else:
            address = None
        if request.form['city']:
            city = request.form['city']
        else:
            city = None
        if request.form['state']:
            state = request.form['state']
        else:
            state = None
        if request.form['zipcode']:
            zipCode = request.form['zipcode']
        else:
            zipCode = None
        if request.form['website']:
            website = request.form['website']
        else:
            website = None
        if request.form['maxcap']:
            maxcap = request.form['maxcap']
        else:
            maxcap = 0
        new_shelter = Shelter(name=name, address=address, city=city,
                              state=state, zipCode=zipCode, website=website,
                              maximum_capacity=maxcap)
        db_session.add(new_shelter)
        db_session.commit()
        print("Shelter created!")
        flash("Shelter created!")
        return redirect(url_for('shelters'))
    else:
        return render_template('newshelter.html')


@app.route('/shelters/<int:shelter_id>/edit', methods=['GET', 'POST'])
def edit_shelter(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['name'] != shelter.name:
            shelter.name = request.form['name']
        if request.form['address'] and request.form['address'] != shelter.address:
            shelter.address = request.form['address']
        if request.form['city'] and request.form['city'] != shelter.city:
            shelter.city = request.form['city']
        if request.form['state'] and request.form['state'] != shelter.state:
            shelter.state = request.form['state']
        if request.form['zipcode'] and request.form['zipcode'] != shelter.zipCode:
            shelter.zipCode = request.form['zipcode']
        if request.form['website'] and request.form['website'] != shelter.website:
            shelter.website = request.form['website']
        if request.form['maxcap'] and request.form['maxcap'] != shelter.maximum_capacity:
            shelter.maximum_capacity = request.form['maxcap']

        db_session.add(shelter)
        db_session.commit()
        print("Shelter {} edited!".format(shelter_id))
        flash("Shelter {} edited!".format(shelter_id))
        return redirect(url_for('shelters'))
    else:
        return render_template('editshelter.html', shelter=shelter)


@app.route('/puppies', defaults={'page': 1})
@app.route('/puppies/page/<int:page>')
def puppies(page):
    count = count_all_puppies()
    puppies = get_puppies_for_page(page, PER_PAGE, count)
    if not puppies and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('puppies.html', pagination=pagination,
                           puppies=puppies)


@app.route('/puppies/new', methods=['GET', 'POST'])
def new_puppy():
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
        else:
            raise AttributeError("name must not be null!")
        if request.form['weight']:
            weight = request.form['weight']
        else:
            weight = None
        if request.form['dateOfBirth']:
            dateOfBirth = request.form['dateOfBirth']
            dtm = datetime.strptime(dateOfBirth, '%Y-%m-%d')
            dateOfBirth = datetime.date(dtm)
        else:
            dateOfBirth = None
        if request.form['gender']:
            gender = request.form['gender']
        else:
            gender = None
        # Profile info
        if request.form['picture']:
            picture = request.form['picture']
        else:
            picture = None
        if request.form['description']:
            description = request.form['description']
        else:
            description = None
        if request.form['specialneeds']:
            specialNeeds = request.form['specialneeds']
        else:
            specialNeeds = None

        new_profile = PuppyProfile(picture=picture, description=description,
                                   specialNeeds=specialNeeds)
        new_puppy = Puppy(name=name, weight=weight, dateOfBirth=dateOfBirth,
                          gender=gender, profile=new_profile)
        db_session.add(new_puppy)
        db_session.commit()
        print("New puppy created!")
        flash("New puppy created!")
        return redirect(url_for('puppies'))
    else:
        return render_template('newpuppy.html')


@app.route('/puppies/<int:puppy_id>/edit', methods=['GET', 'POST'])
def edit_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    if request.method == 'POST':
        if request.form['name']:
            puppy.name = request.form['name']
        if request.form['weight']:
            puppy.weight = request.form['weight']
        if request.form['dateOfBirth']:
            dateOfBirth = request.form['dateOfBirth']
            dtm = datetime.strptime(dateOfBirth, '%Y-%m-%d')
            puppy.dateOfBirth = datetime.date(dtm)
        if request.form['gender']:
            puppy.gender = request.form['gender']
        # Profile info
        if puppy.profile:
            if request.form['picture']:
                puppy.profile.picture = request.form['picture']
            if request.form['description']:
                puppy.profile.description = request.form['description']
            if request.form['specialneeds']:
                puppy.profile.specialNeeds = request.form['specialneeds']
        else:
            if request.form['picture']:
                picture = request.form['picture']
            else:
                picture = None
            if request.form['description']:
                description = request.form['description']
            else:
                description = None
            if request.form['specialneeds']:
                specialNeeds = request.form['specialneeds']
            else:
                specialNeeds = None
            new_profile = PuppyProfile(picture=picture,
                                       description=description,
                                       specialNeeds=specialNeeds)
            puppy.profile = new_profile


        db_session.add(puppy)
        db_session.commit()
        print("Puppy {} edited!".format(puppy_id))
        flash("Puppy {} edited!".format(puppy_id))
        return redirect(url_for('puppies'))
    else:
        return render_template('editpuppy.html', puppy=puppy)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
