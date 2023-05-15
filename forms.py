from wsgiref import validate

from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, EqualTo


# Create a form  class
class registerForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()],render_kw={"placeholder": "Full Name"})
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    mobile=StringField("Mobile", validators=[DataRequired()])
    password_hash=PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must Match')])
    password_hash2=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Submit')


# Create a login form
class LoginForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField('Login')


class UpdateForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    mobile=StringField("Mobile", validators=[DataRequired()])
    submit=SubmitField('Update')



class SearchForm(FlaskForm):
    search=StringField("Search", validators=[DataRequired()])
    submit=SubmitField('Search')


class Dailyreportform(FlaskForm):
    item_name=StringField("Item Name", validators=[DataRequired()])
    buying_price=IntegerField("Buying Price", validators=[DataRequired()])
    selling_price=IntegerField("Selling Price", validators=[DataRequired()])
    remarks=StringField("Remarks")
    submit=SubmitField('Submit')


class Daybookform(FlaskForm):
    date=DateField('Datepicker', format='%Y-%m-%d',validators=[DataRequired()])
    submit=SubmitField('Submit')


class UserForm(FlaskForm):
    service_type=StringField("Service Type", validators=[DataRequired()])
    product_name=StringField("Product Name", validators=[DataRequired()])
    serial_no=StringField("Serial No", validators=[DataRequired()])
    customer_name=StringField("Customer Name", validators=[DataRequired()])
    customer_mobile=StringField("Customer Mobile", validators=[DataRequired()])
    customer_email=StringField("Customer Email", validators=[DataRequired()])
    customer_address=StringField("Customer Address", validators=[DataRequired()])
    service_cost=IntegerField("Service Cost", validators=[DataRequired()])
    remarks=StringField("Remarks")
    submit=SubmitField('ADD')


class EditForm(FlaskForm):
    service_type=StringField("Service Type")
    product_name=StringField("Product Name")
    serial_no=StringField("Serial No")
    customer_name=StringField("Customer Name")
    customer_mobile=StringField("Customer Mobile")
    customer_email=StringField("Customer Email")
    customer_address=StringField("Customer Address")
    service_cost=IntegerField("Service Cost")
    remarks=StringField("Remarks")
    submit=SubmitField('Update')

