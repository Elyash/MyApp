from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, URL, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class GiftForm(FlaskForm):
    name = StringField('Gift Name', validators=[DataRequired()])
    image_url = StringField('Gift Image URL', validators=[DataRequired(), URL()])
    buy_link = StringField('Link to Buy (Optional)', validators=[URL()])
    cost = FloatField('Gift Cost', validators=[DataRequired()])
    submit = SubmitField('Upload Gift')
