"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user():
    return auth.current_user.get('id') if auth.current_user else None


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'stats',
    Field('school', requires=IS_IN_SET(['UC Santa Cruz', 'UC Los Angeles', 'UC Irvine',
                                        'UC San Diego', 'UC Berkeley', 'UC Santa Barbara',
                                        'UC Riverside', 'UC Merced', 'UC Davis'])),
    Field('grad_year', 'integer', default=0),
    Field('major'),
    Field('sat_score', 'integer', default=0),
    Field('act_score', 'integer', default=0),
    Field('gpa', 'float', default=0.0),
    Field('student', 'reference auth_user', default=get_user),
)
db.stats.student.readable = db.stats.student.writable = False
db.stats.id.readable = db.stats.id.writable = False

db.define_table(
    'reviews',
    Field('rating_weight'),  # 1 or 0, would the user come here again?
    Field('positive_review'),  # 1 positive experience they had
    Field('negative_review'),  # 1 negative experience they had
    Field('student', 'reference auth_user', default=get_user),
)

db.define_table(
    'schools',
    Field('school_name', notnull=True),
    Field('school_address', notnull=True),
    Field('school_email', notnull=True),
)

#insert into schools

#UCSC
db.schools.insert(
    school_name='University of California, Santa Cruz',   #school_name
    school_address='1156 High St., Santa Cruz, CA 95064', 
    school_email='@ucsc.edu')
#UCB
db.schools.insert(
    school_name='University of California, Berkeley',   #school_name
    school_address='200 Centennial Dr., Berkeley, California 94720', 
    school_email='@berkeley.edu')
#UCLA
db.schools.insert(
    school_name='University of California, Los Angeles',   #school_name
    school_address='405 Hilgard Ave., Los Angeles, CA 94720', 
    school_email='@ucla.edu')
#UCSD
db.schools.insert(
    school_name='University of California, San Diego', 
    school_address='9500 Gilman Dr., La Jolla, CA 92093',
    school_email='@ucsd.edu')
#UCR
db.schools.insert(
    school_name='University of California, Riverside', 
    school_address='900 University Ave., Riverside, CA 92521',
    school_email='@ucr.edu')
#UCD
db.schools.insert(
    school_name='University of California, Davis', 
    school_address='1 Shields Ave., Davis, CA 95616',
    school_email='@ucdavis.edu')
#UCI
db.schools.insert(
    school_name='University of California, Irvine', 
    school_address='Irvine, CA 92697',
    school_email='@uci.edu')
#UCM
db.schools.insert(
    school_name='University of California, Merced', 
    school_address='5200 Lake Rd., Merced, CA 95343',
    school_email='@ucm.edu')
#UCSF
db.schools.insert(
    school_name='University of California, Riverside', 
    school_address='505 parnassus Ave., San Francisco, CA 94143',
    school_email='@ucsf.edu')
#UCSB
db.schools.insert(
    school_name='University of California, Santa Barbara', 
    school_address='Santa Barbara, CA 93106',
    school_email='@ucsb.edu')

db.commit()
