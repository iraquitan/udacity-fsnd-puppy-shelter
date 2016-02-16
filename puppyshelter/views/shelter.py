# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: shelter
 * Date: 2/16/16
 * Time: 12:15 AM
"""
from puppyshelter import app
from flask import request, render_template, redirect, abort, flash, url_for
from puppyshelter import db
from puppyshelter.forms import ShelterForm
from puppyshelter.models import Shelter


@app.route('/shelters', defaults={'page': 1})
@app.route('/shelters/', defaults={'page': 1})
@app.route('/shelters/page/<int:page>')
def shelters(page):
    shelters = Shelter.query.paginate(page, app.config['POSTS_PER_PAGE'],
                                      False)
    if not shelters and page != 1:
        abort(404)
    return render_template('shelters.html', pagination=shelters,
                           shelters=shelters.items)


@app.route('/shelters/new', methods=['GET', 'POST'])
def new_shelter():
    form = ShelterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # if request.form['name']:
        #     name = request.form['name']
        # else:
        #     raise AttributeError("name must not be null!")
        # if request.form['address']:
        #     address = request.form['address']
        # else:
        #     address = None
        # if request.form['city']:
        #     city = request.form['city']
        # else:
        #     city = None
        # if request.form['state']:
        #     state = request.form['state']
        # else:
        #     state = None
        # if request.form['zipcode']:
        #     zipCode = request.form['zipcode']
        # else:
        #     zipCode = None
        # if request.form['website']:
        #     website = request.form['website']
        # else:
        #     website = None
        # if request.form['maxcap']:
        #     maxcap = request.form['maxcap']
        # else:
        #     maxcap = 0
        new_shelter = Shelter(name=form.name.data,
                              address=form.address['address'].data,
                              city=form.address['city'].data,
                              state=form.address['state'].data,
                              zipCode=form.address['zip_code'].data,
                              website=form.website.data,
                              maximum_capacity=form.maximum_capacity.data)
        db.session.add(new_shelter)
        db.session.commit()
        print("Shelter created!")
        flash("Shelter created!")
        return redirect(url_for('shelters'))
    else:
        return render_template('newshelter.html', form=form)


@app.route('/shelters/<int:shelter_id>/edit', methods=['GET', 'POST'])
def edit_shelter(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    form = ShelterForm(obj=shelter)
    form.address['address'].data = shelter.address
    form.address['city'].data = shelter.city
    form.address['state'].data = shelter.state
    form.address['zip_code'].data = shelter.zipCode
    if request.method == 'POST' and form.validate_on_submit():
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
        return render_template('editshelter.html', shelter=shelter, form=form)


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
