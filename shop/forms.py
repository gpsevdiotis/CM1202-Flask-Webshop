from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired, NumberRange
from shop.models import User
from datetime import date
import re


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,15}$',
                              message='Your password should be between 6 and 15 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
  comment = StringField('Comment',validators=[InputRequired()])
  submit = SubmitField('Post comment')

class CheckoutForm(FlaskForm):
    name = StringField("Full name", validators=[InputRequired('Please enter a name'), Length(min =0, max=35, message="Must be less than 35 characters")])
    adrline1 = StringField("Address line 1", validators=[InputRequired('Please enter the first line of your address'), Length(min =0, max=35, message="Must be less than 35 characters")])
    adrline2 = StringField("Address line 2", validators=[Length(min=0, max=35, message="Must be less than 35 characters")])
    city = StringField("City/Town", validators=[InputRequired('Please enter the post town'), Length(min =0, max=35, message="Must be less than 35 characters")])
    postcode = StringField("Postcode", validators=[InputRequired('Please enter a postcode'), Length(min=5, max=8, message="Incorrect length")])
    cardnumber = IntegerField("Card Number", validators=[InputRequired('Please enter your card number'), NumberRange(min = 100000000000000, max = 9999999999999999, message = "Card number must be 16 digits.")])
    expiryyear = IntegerField("Year of expiry", validators=[InputRequired('Please enter a year of expiry'), NumberRange(min=date.today().year, max = date.today().year + 100, message = "Must be current year or in near future")])
    expirymonth = SelectField("Month of expiry", choices=[(1, "Jan"), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9,'Sep'), (10, 'Oct'), (11, 'Nov'), (12,'Dec')], coerce = int)
    cardname = StringField("Name on card", validators=[InputRequired('Please enter the name on the card'), Length(min = 0, max=22, message = "Cannot be longer than 22 characters")])
    cvv = IntegerField("Card security code", validators=[InputRequired('Please enter your card security number'), NumberRange(min=100, max=9999, message = "Must be 3 or 4 digits")])
    submit = SubmitField('Confirm Purchase', validators=[InputRequired()])

    def validate_expirymonth(self, expirymonth):
        if self.expiryyear.data == date.today().year:
            if expirymonth.data < date.today().month:
                raise ValidationError('This date is in the past')

    def validate_postcode(self, postcode):
        inward = postcode.data[-3:].upper()
        outward = postcode.data[0:-3].strip().upper()
        inwardpass = False
        outwardpass = False
        if inward[0].isdigit() == True and inward[1:].isalpha() == True:
            for char in ["C", "I", "K", "M", "O", "V"]:
                if char in inward:
                    pass
                else:
                    inwardpass = True
                    break
            codecombos = [r"^[A-Z][0-9]", r"^[A-Z][0-9]", r"^[A-Z][A-Z][0-9]", r"^[A-Z][A-Z][0-9][0-9]", r"^[A-Z][0-9][A-Z]", r"^[A-Z][A-Z][0-9][A-Z]", r"^[A-Z][A-Z][A-Z]"]
            for combo in codecombos:
                if re.match(combo, outward) != None:
                    outwardpass = True
                    break
        if inwardpass == False or outwardpass == False:
            raise ValidationError('Invalid postcode')
