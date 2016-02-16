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
    TextAreaField, FormField, IntegerField, DecimalField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, InputRequired, Regexp, NumberRange, \
    Optional


class AddressForm(Form):
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('Zip Code')


class PuppyProfileForm(Form):
    picture = URLField('Picture URL', validators=[url(), Optional()])
    description = TextAreaField('Puppy description', validators=[Optional()])
    special_needs = TextAreaField('Puppy special needs',
                                  validators=[Optional()])


class PuppyForm(Form):
    name = StringField('Puppy name', [InputRequired(
                                          message='Puppy name is required'),
                                      Regexp('[A-Z]{1}[a-z]*',
                                             message='Should start with '
                                                     'uppercase letter')])
    weight = DecimalField('Puppy weight', [NumberRange(
        min=0, message='Weight must be positive'), Optional()])
    date_of_birth = DateField('Date of birth', [Optional()])
    gender = SelectField('Gender', choices=[('female', 'Female'),
                                            ('male', 'Male')])
    profile = FormField(PuppyProfileForm)
    shelter = SelectField('Shelter', choices=[(0, 'None')], coerce=int,
                          default=0)


class ShelterForm(Form):
    name = StringField('Name', [
        InputRequired(message='Shelter name is required')])
    address = FormField(AddressForm)
    website = URLField('Website URL', validators=[url(), Optional()])
    maximum_capacity = IntegerField('Maximum capacity', [NumberRange(
        min=1, message='Capacity must be positive')],
                                    default=25)
