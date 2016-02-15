# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: views
 * Date: 2/14/16
 * Time: 12:33 PM
"""
from puppyshelter import app
from datetime import datetime
from flask import request, render_template, redirect, abort, flash, \
    url_for
from .control import get_carousel_puppies
from .forms import PuppyForm
from . import db
from .models import Adopter, Puppy, PuppyProfile, Shelter


@app.route('/')
@app.route('/index')
@app.route('/index/')
def index():
    puppies = get_carousel_puppies()
    return render_template('index.html', puppies=puppies)


@app.route('/shelters')
@app.route('/shelters/')
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
        db.session.add(new_shelter)
        db.session.commit()
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

        db.session.add(shelter)
        db.session.commit()
        print("Shelter {} edited!".format(shelter_id))
        flash("Shelter {} edited!".format(shelter_id))
        return redirect(url_for('shelters'))
    else:
        return render_template('editshelter.html', shelter=shelter)


@app.route('/shelters/<int:shelter_id>/delete', methods=['GET', 'POST'])
def delete_shelter(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    if request.method == 'POST':
        db.session.delete(shelter)
        db.session.commit()
        print("Puppy {} deleted!".format(shelter_id))
        flash("Puppy {} deleted!".format(shelter_id))
        return redirect(url_for('shelters'))
    else:
        return render_template('deleteshelter.html', shelter=shelter)


@app.route('/puppies', defaults={'page': 1})
@app.route('/puppies/', defaults={'page': 1})
@app.route('/puppies/page/<int:page>')
def puppies(page):
    puppies = Puppy.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
    if not puppies and page != 1:
        abort(404)
    return render_template('puppies.html', pagination=puppies,
                           puppies=puppies.items)


@app.route('/puppies/<int:puppy_id>/profile')
def puppy_profile(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    return render_template('puppyprofile.html', puppy=puppy)


@app.route('/puppies/new', methods=['GET', 'POST'])
def new_puppy():
    shelters = Shelter.query.all()
    form = PuppyForm(request.form)
    form.shelter.choices = form.shelter.choices + [
        (sh.id, sh.name)
        for sh in shelters
        if sh.maximum_capacity > sh.current_occupancy]
    if request.method == 'POST' and form.validate():
        new_profile = PuppyProfile(picture=form.profile.picture.data,
                                   description=form.profile.description.data,
                                   specialNeeds=form.profile.special_needs.data)
        if form.shelter.data and form.shelter.data != 0:
            shelter = Shelter.query.filter_by(id=form.shelter.data).one()
            shelter.current_occupancy += 1
            db.session.add(shelter)
        else:
            shelter = None
        new_puppy = Puppy(name=form.name.data, weight=form.weight.data,
                          dateOfBirth=form.date_of_birth.data,
                          gender=form.gender.data, profile=new_profile,
                          shelter=shelter)
        db.session.add(new_puppy)
        db.session.commit()
        print("New puppy created!")
        flash("New puppy created!")
        return redirect(url_for('puppies'))
    else:
        return render_template('newpuppy.html', form=form)


@app.route('/puppies/<int:puppy_id>/edit', methods=['GET', 'POST'])
def edit_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    shelters = Shelter.query.all()
    form = PuppyForm(obj=puppy)
    form.shelter.choices = form.shelter.choices + [
        (sh.id, sh.name)
        for sh in shelters
        if sh.maximum_capacity > sh.current_occupancy]
    form.date_of_birth.data = puppy.dateOfBirth
    form.profile['picture'].data = puppy.profile.picture
    form.profile['description'].data = puppy.profile.description
    form.profile['special_needs'].data = puppy.profile.specialNeeds
    form.shelter.data = puppy.shelter_id
    # form.shelter.default = puppy.shelter_id
    if request.method == 'POST' and form.validate():
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
        if 'shelter' in request.form.keys():
            if request.form['shelter']:
                shelter = Shelter.query.filter_by(id=request.form['shelter']).one()
                puppy.shelter = shelter
                shelter.current_occupancy += 1
                db.session.add(shelter)
        db.session.add(puppy)
        db.session.commit()
        print("Puppy {} edited!".format(puppy_id))
        flash("Puppy {} edited!".format(puppy_id))
        return redirect(url_for('puppies'))
    else:
        return render_template('editpuppy.html', form=form, puppy=puppy)


@app.route('/puppies/<int:puppy_id>/adopt', methods=['GET', 'POST'])
def adopt_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    users = Adopter.query.all()
    if request.method == 'POST':
        if request.form['sel-users']:
            for adopter_id in request.form.getlist('sel-users'):
                adopter = Adopter.query.filter_by(id=adopter_id).one()
                puppy.adopters.append(adopter)
            puppy_shelter = puppy.shelter
            puppy_shelter.puppies.remove(puppy)  # remove puppy from shelter
            puppy_shelter.current_occupancy -= 1  # update current occupancy
            db.session.add(puppy)  # update puppy
            db.session.add(puppy_shelter)  # update shelter
            db.session.commit()
            print("Puppy {} adopted!".format(puppy_id))
            flash("Puppy {} adopted!".format(puppy_id))
            return redirect(url_for('puppies'))
    else:
        return render_template('adoptpuppy.html', puppy=puppy, users=users)


@app.route('/puppies/<int:puppy_id>/delete', methods=['GET', 'POST'])
def delete_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    if request.method == 'POST':
        if puppy.shelter:
            shelter = puppy.shelter
            shelter.current_occupancy -= 1
            db.session.add(shelter)
        db.session.delete(puppy)
        db.session.commit()
        print("Puppy {} deleted!".format(puppy_id))
        flash("Puppy {} deleted!".format(puppy_id))
        return redirect(url_for('puppies'))
    else:
        return render_template('deletepuppy.html', puppy=puppy)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        pass
    else:
        return render_template('newuser.html')