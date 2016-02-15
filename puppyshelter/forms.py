# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: forms
 * Date: 2/14/16
 * Time: 10:24 PM
"""
from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, FloatField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.fields.html5 import URLField


class NewPuppy(Form):
    name = StringField('Puppy name', [#validators.Length(min=4, max=25),
                                      validators.InputRequired(
                                          message='Puppy name is required'),
                                      validators.Regexp(
                                          '[A-Z]{1}[a-z]*', message='Must start with CAPS')])
    weight = FloatField('Puppy weight', [validators.NumberRange(
        min=0, message='Weight must be positive'), validators.Optional()])
    date_of_birth = DateField('Date of birth', [validators.Optional()])
    gender = SelectField('Gender', choices=[('female', 'Female'),
                                            ('male', 'Male')])
    picture = URLField('Picture URL')
    description = TextAreaField('Puppy description')
    special_needs = TextAreaField('Puppy special needs')
    shelter = SelectField('Shelter', coerce=int)
