# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: control
 * Date: 2/10/16
 * Time: 1:59 AM
"""
import random
from sqlalchemy import func
from math import ceil
from .database import db_session
from .models import Puppy


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
                    (self.page - left_current - 1 < num < self.page + right_current) \
                    or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def count_all_puppies():
    count = db_session.query(func.count(Puppy.id)).scalar()
    return count


def get_puppies_for_page(page, per_page, count):
    puppies = db_session.query(Puppy).slice((page-1) * per_page,
                                            (page-1) * per_page + per_page)
    return puppies


def get_carousel_puppies():
    puppies = []
    puppy_ids = db_session.query(Puppy.id).all()
    for i in range(3):
        rand_id = random.choice(puppy_ids)
        puppy_ids.remove(rand_id)  # prevent getting the same puppy
        puppies.append(db_session.query(Puppy).filter_by(id=rand_id[0]).one())
    return puppies
