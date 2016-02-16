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
from flask import request, render_template
from puppyshelter.control import get_carousel_puppies


@app.route('/')
@app.route('/index')
@app.route('/index/')
def index():
    puppies = get_carousel_puppies()
    return render_template('index.html', puppies=puppies)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        pass
    else:
        return render_template('newuser.html')