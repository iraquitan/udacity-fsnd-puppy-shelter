# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: puppy
 * Date: 2/16/16
 * Time: 12:17 AM
"""
from logging.handlers import RotatingFileHandler

from flask.ext.mail import Message

from puppyshelter import app, mail
from flask import request, render_template, redirect, abort, flash, url_for
from puppyshelter.forms import PuppyForm, AdoptPuppyForm
from puppyshelter import db
from puppyshelter.models import Adopter, Puppy, PuppyProfile, Shelter


if app.debug:
    log_file_handler = RotatingFileHandler(
        '../puppy-shelter/puppyshelter/basic-logging.txt',
        maxBytes=1000, backupCount=0)
    app.logger.addHandler(log_file_handler)


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
    if form.validate_on_submit():
        new_profile = PuppyProfile(
            picture=form.profile['picture'].data,
            description=form.profile['description'].data,
            specialNeeds=form.profile['special_needs'].data)
        if form.shelter.data != 0:
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
        if app.debug:
            app.logger.debug("Puppy {} created!".format(
                (new_puppy.id, new_puppy.name)))
        flash("Puppy {} created!".format((new_puppy.id, new_puppy.name)))
        return redirect(url_for('puppies'))
    else:
        return render_template('newpuppy.html', form=form)


@app.route('/puppies/<int:puppy_id>/edit', methods=['GET', 'POST'])
def edit_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    shelters = Shelter.query.all()
    form = PuppyForm(request.form)

    if form.validate_on_submit():
        puppy.name = form.name.data
        puppy.weight = form.weight.data
        puppy.dateOfBirth = form.date_of_birth.data
        puppy.gender = form.gender.data
        # Profile info
        if puppy.profile:
            puppy.profile.picture = form.profile['picture'].data
            puppy.profile.description = form.profile['description'].data
            puppy.profile.specialNeeds = form.profile['special_needs'].data
        else:
            new_profile = PuppyProfile(
                picture=form.profile['picture'].data,
                description=form.profile['description'].data,
                specialNeeds=form.profile['special_needs'].data)
            puppy.profile = new_profile
        if form.shelter.data != 0:
            new_shelter = Shelter.query.filter_by(id=form.shelter.data).one()
            if puppy.shelter:
                old_shelter = puppy.shelter
                old_shelter.current_occupancy -= 1
                db.session.add(old_shelter)
            puppy.shelter = new_shelter
            new_shelter.current_occupancy += 1
            db.session.add(new_shelter)
        else:
            if puppy.shelter:
                old_shelter = puppy.shelter
                old_shelter.current_occupancy -= 1
                db.session.add(old_shelter)
            puppy.shelter = None

        db.session.add(puppy)
        db.session.commit()
        if app.debug:
            app.logger.debug("Puppy {} edited!".format(
                (puppy_id, puppy.name)))
        flash("Puppy {} edited!".format((puppy_id, puppy.name)))
        return redirect(url_for('puppies'))
    else:
        form = PuppyForm(obj=puppy)
        if len(puppy.adopters) > 0:
            del form.shelter
        else:
            form.shelter.choices = form.shelter.choices + [
                    (sh.id, sh.name)
                    for sh in shelters
                    if sh.maximum_capacity > sh.current_occupancy]
            if puppy.shelter:
                form.shelter.data = puppy.shelter_id
            else:
                form.shelter.data = 0
        form.date_of_birth.data = puppy.dateOfBirth
        form.profile['picture'].data = puppy.profile.picture
        form.profile['description'].data = puppy.profile.description
        form.profile['special_needs'].data = puppy.profile.specialNeeds
        return render_template('editpuppy.html', form=form, puppy=puppy)


@app.route('/puppies/<int:puppy_id>/adopt', methods=['GET', 'POST'])
def adopt_puppy(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    users = Adopter.query.all()
    form = AdoptPuppyForm(request.form)
    form.adopters.choices = [(user.id, user.name) for user in users]
    if form.validate_on_submit():
        for adopter_id in form.adopters.data:
            adopter = Adopter.query.filter_by(id=adopter_id).one()
            puppy.adopters.append(adopter)
        puppy_shelter = puppy.shelter
        puppy_shelter.puppies.remove(puppy)  # remove puppy from shelter
        puppy_shelter.current_occupancy -= 1  # update current occupancy
        db.session.add(puppy)  # update puppy
        db.session.add(puppy_shelter)  # update shelter
        db.session.commit()
        if app.debug:
            app.logger.debug("Puppy {} adopted!".format(
                (puppy_id, puppy.name)))
        flash("Puppy {} adopted!".format(
            (puppy_id, puppy.name)))
        return redirect(url_for('puppies'))
    else:
        return render_template('adoptpuppy.html', puppy=puppy, form=form)


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
        if app.debug:
            app.logger.debug("Puppy {} deleted!".format(
                (puppy_id, puppy.name)))
        flash("Puppy {} deleted!".format((puppy_id, puppy.name)))
        return redirect(url_for('puppies'))
    else:
        return render_template('deletepuppy.html', puppy=puppy)
