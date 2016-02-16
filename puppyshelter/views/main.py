# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: views
 * Date: 2/14/16
 * Time: 12:33 PM
"""
from logging.handlers import RotatingFileHandler

from puppyshelter import app, db
from flask import request, render_template, flash, url_for, redirect
from puppyshelter.control import get_carousel_puppies
from puppyshelter.forms import UserForm
from puppyshelter.models import Adopter


if app.debug:
    log_file_handler = RotatingFileHandler(
        '../puppy-shelter/puppyshelter/basic-logging.txt',
        maxBytes=1000, backupCount=0)
    app.logger.addHandler(log_file_handler)


@app.route('/')
@app.route('/index')
@app.route('/index/')
def index():
    puppies = get_carousel_puppies()
    return render_template('index.html', puppies=puppies)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = Adopter(name=form.name.data, gender=form.gender.data,
                       address=form.address['address'].data,
                       city=form.address['city'].data,
                       state=form.address['state'].data,
                       zipCode=form.address['zip_code'].data,
                       dateOfBirth=form.date_of_birth.data,
                       email=form.email.data)
        db.session.add(user)
        db.session.commit()
        if app.debug:
            app.logger.debug("User {} edited!".format(
                (user.id, user.name)))
        flash("User {} edited!".format(
            (user.id, user.name)))
        return redirect(url_for('index'))
    else:
        return render_template('newuser.html', form=form)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Adopter.query.filter_by(id=user_id).one()
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.gender = form.gender.data
        user.address = form.address['address'].data
        user.city = form.address['city'].data
        user.state = form.address['state'].data
        user.zipCode = form.address['zip_code'].data
        user.dateOfBirth = form.date_of_birth.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        if app.debug:
            app.logger.debug("User {} edited!".format(
                (user_id, user.name)))
        flash("User {} edited!".format(
            (user_id, user.name)))
        return redirect(url_for('index'))
    else:
        form.date_of_birth.data = user.dateOfBirth
        form.address['address'].data = user.address
        form.address['city'].data = user.city
        form.address['state'].data = user.state
        form.address['zip_code'].data = user.zipCode
        return render_template('edituser.html', form=form, user=user)
