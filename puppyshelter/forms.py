# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: forms
 * Date: 2/14/16
 * Time: 10:24 PM
"""
from flask_wtf import Form
from wtforms import StringField, FloatField, DateField, SelectField, \
    TextAreaField, FormField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, InputRequired, Regexp, NumberRange, \
    Optional


class PuppyProfileForm(Form):
    picture = URLField('Picture URL', validators=[url(), Optional()])
    description = TextAreaField('Puppy description')
    special_needs = TextAreaField('Puppy special needs')


class PuppyForm(Form):
    name = StringField('Puppy name', [InputRequired(
                                          message='Puppy name is required'),
                                      Regexp('[A-Z]{1}[a-z]*',
                                             message='Should start with '
                                                     'uppercase letter')])
    weight = FloatField('Puppy weight', [NumberRange(
        min=0, message='Weight must be positive'), Optional()])
    date_of_birth = DateField('Date of birth', [Optional()])
    gender = SelectField('Gender', choices=[('female', 'Female'),
                                            ('male', 'Male')])
    profile = FormField(PuppyProfileForm)
    shelter = SelectField('Shelter', choices=[(0, 'None')], coerce=int,
                          default=0)
