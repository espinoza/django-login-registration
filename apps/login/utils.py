import re
from datetime import date

def contains_digit(string):
    RE_digit = re.compile('\d')
    return RE_digit.search(string)


def contains_uppercase(string):
    RE_upper = re.compile('[A-Z]')
    return RE_upper.search(string)


def is_valid_email(email):
    RE_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    return RE_EMAIL.match(email)


def get_age(birthDate):
    today = date.today()
    date_is_before_birthday = (today.month, today.day) \
                               < (birthDate.month, birthDate.day)
    age = today.year - birthDate.year - date_is_before_birthday
    return age


def is_past(a_date):
    return a_date < date.today() 


def is_valid_rut(rut):
    RE_EMAIL = re.compile(r'^[\d]{1,2}\.[\d]{3}\.[\d]{3}-[\dkK]{1}$')
    return RE_EMAIL.match(rut)


