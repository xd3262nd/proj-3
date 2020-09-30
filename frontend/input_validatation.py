
from peewee_validates import Validator, StringField, validate_not_empty, validate_length, validate_email, \
    validate_regexp, validate_one_of, DecimalField, validate_range


class SimpleValidator(Validator):
    name = StringField(validators=[validate_not_empty(), validate_length(3, 99), validate_regexp('^[a-zA-Z ]*$')])
    email = StringField(validators=[validate_email()])
    art_name = StringField(validators=[validate_not_empty(), validate_length(3, 99)])
    art_price = DecimalField(validators=[validate_not_empty(), validate_range(1, 9999)])
    availability = StringField(validators=[validate_one_of(['yes', 'no'])])


VALIDATOR = SimpleValidator()


def validate_name(name):
    validation = VALIDATOR.validate({'name': name.strip()})

    while not validation:
        name = input('Invalid input. Please re-enter the artist name (only alphabet and must have more than 2 '
                     'characters):\t\t')
        validation = VALIDATOR.validate({'name': name.strip()})
    return name


def validate_email_address(email):
    validation = VALIDATOR.validate({'email': email.strip()})
    while not validation:
        email = input('Invalid input. Please re-enter a proper email address.\t\t')
        validation = VALIDATOR.validate({'email': email.strip()})
    return email


def validate_artname(art_name):
    validation = VALIDATOR.validate({'art_name': art_name.strip()})
    while not validation:
        art_name = input('Invalid input. Please re-enter a new artwork name.\t\t')
        validation = VALIDATOR.validate({'art_name': art_name.strip()})
    return art_name


def validate_price(art_price):
    validation = VALIDATOR.validate({'art_price': art_price})
    while not validation:
        art_price = input('Invalid input. Please re-enter a new price that is more than 1 and less than 9999.\t\t')
        validation = VALIDATOR.validate({'art_price': art_price})
    return art_price


def validate_availability(availability):

    validation = VALIDATOR.validate({'availability': availability.strip().lower()})
    while not validation:
        availability = input('Invalid input. Please enter either yes or no for the artwork availability.\t\t')
        validation = VALIDATOR.validate({'availability': availability.strip().lower()})
    if availability.lower() == 'yes':
        availability_bool = True
    elif availability.lower() == 'no':
        availability_bool = False
    else:
        return

    return availability_bool
