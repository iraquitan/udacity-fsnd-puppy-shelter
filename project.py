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


@app.route('/puppy/new', methods=['GET', 'POST'])
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

        if request.form['picture']:
            picture = request.form['picture']
        else:
            picture = None
        if request.form['description']:
            description = request.form['description']
        else:
            description = None
        if request.form['specialNeeds']:
            specialNeeds = request.form['specialNeeds']
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


@app.route('/puppy/<int:puppy_id>/edit', methods=['GET', 'POST'])
def edit_puppy(puppy_id):
    puppy = Puppy.query.filter(id=puppy_id)
    if request.method == 'POST':
        pass
    else:
        return render_template('editpuppy.html', puppy=puppy)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
