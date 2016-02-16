# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: __init__
 * Date: 2/8/16
 * Time: 2:46 PM
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
import puppyshelter.views.main
import puppyshelter.views.puppy
import puppyshelter.views.shelter
