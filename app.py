from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import (Dailyreportform, Daybookform, EditForm, LoginForm,
                   SearchForm, UpdateForm, UserForm, registerForm)
from werkzeug.security import check_password_hash, generate_password_hash

app= Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'
#Add DataBase mysql
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://rahul:password123@localhost/users'
app.config['SECRET_KEY']="this is my secret key"
db = SQLAlchemy(app)
migrate=Migrate(app,db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#Create a String
def __repr__(self):
    return '<Name %r>' % self.name




#######################################################################


@app.route("/")
def index():
    return redirect(url_for('login'))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/dashboard")
@login_required
def dashboard():
    form=services()
    name=current_user.name
    return render_template('dashboard.html',name=name,form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("505.html"), 505

######################################################################################################################

##### LOGIN USER #####


@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash,form.password.data):
            login_user(user)
            name=user.name
            name=user.name
            return redirect(url_for('addrecord',name=name))

        else:
            flash("Invalid username or password")
    return render_template('login.html',form=form)


#### REGISTER USER #####


@app.route("/XYZ123456",methods=['GET','POST'])
def signup():
    form= registerForm()
    name=form.name.data    
    if form.validate_on_submit():
        #Create a user
        if form.password_hash.data == form.password_hash2.data:
            if Users.query.filter_by(username=form.username.data).first():
                flash("Username already exist")
                return redirect(url_for('signup',name=name))
            else:
                hash_password=generate_password_hash(form.password_hash.data,method='sha256')
                new_user=Users(name=form.name.data,username=form.username.data,email=form.email.data,mobile=form.mobile.data,password_hash=hash_password)
                db.session.add(new_user)
                db.session.commit()
                form.name.data=''
                form.username.data=''
                form.email.data=''
                form.mobile.data=''
                form.password_hash.data=''
                form.password_hash2.data=''

                flash("User Created Successfully")
                return redirect(url_for('login',name=name))
        else:
            flash("Password does not match")
            return redirect(url_for('signup',name=name))
    return render_template('signup.html',form=form,name=name)


##### UPDATE USER #####

@app.route('/update',methods=['GET','POST'])
@login_required
def update():
    name=current_user.name
    id=current_user.id
    user_to_update=Users.query.order_by(Users.id.desc()).first()
    form=UpdateForm()
    old_data=Users.query.get(id)
    if form.validate_on_submit():
        user_to_update.name=form.name.data
        user_to_update.username=form.username.data
        user_to_update.email=form.email.data
        user_to_update.mobile=form.mobile.data
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('addrecord',name=name))
    return render_template('update.html',form=form,name=name,id=id,old_data=old_data)

        




##### DELETE USER #####


@app.route("/deleteuser")
@login_required
def deleteuser():
    id=current_user.id
    user_to_delete=Users.query.order_by(Users.id.desc()).first()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('login'))
    except:
        flash("There was a problem deleting that user")
        return redirect(url_for('dashboard'))


######################################################################################################################


##### ADD RECORD  #####


@app.route("/addrecord",methods=['GET','POST'])
@login_required
def addrecord():
    name=current_user.name
    form=UserForm()
    if form.validate_on_submit():
        service=services(customer_name=form.customer_name.data,customer_mobile=form.customer_mobile.data,customer_email=form.customer_email.data,customer_address=form.customer_address.data,remarks=form.remarks.data,serial_no=form.serial_no.data,product_name=form.product_name.data,service_cost=form.service_cost.data,service_type=form.service_type.data)
        db.session.add(service)
        db.session.commit()
        flash('Record added successfully')
        return redirect(url_for('addrecord',name=name))
    else:
        print(form.errors)
    return render_template('addrecord.html',form=form,name=name)


##### VIEW RECORD  #####

@app.route("/viewrecord",methods=['GET','POST'])
@login_required
def viewrecord():
    form=SearchForm()
    name=current_user.name
    service=services.query.all()
    

    return render_template('viewrecord.html',service=service,name=name,form=form)


##### EDIT RECORD #####

@app.route("/editrecord/<int:id>",methods=['GET','POST'])
@login_required
def editrecord(id):
    form=EditForm()
    name=current_user.name
    previous_record=services.query.select_from(services).filter_by(id=id).first()   
    if form.validate_on_submit():
        service=services.query.select_from(services).filter_by(id=id).first()
        service.customer_name=form.customer_name.data
        service.customer_mobile=form.customer_mobile.data
        service.customer_address=form.customer_address.data
        service.customer_email=form.customer_email.data
        service.serial_no=form.serial_no.data
        service.product_name=form.product_name.data
        service.service_type=form.service_type.data
        service.service_cost=form.service_cost.data
        service.remarks=form.remarks.data
        db.session.commit()
        flash("Record updated successfully")
        return redirect(url_for('viewrecord',name=name))
    else:
        print(form.errors)
    return render_template('editrecord.html',name=name,form=form,previous_record=previous_record)


##### DELETE RECORD #####

@app.route("/deleterecord/<int:id>")
@login_required
def deleterecord(id):
    name=current_user.name
    service=services.query.select_from(services).filter_by(id=id).first()
    try:
        db.session.delete(service)
        db.session.commit()
        return redirect(url_for('viewrecord',name=name))
    except:
        flash("There was a problem deleting that record")
        return redirect(url_for('viewrecord',name=name))
    
######################################################################################################################


##### DAILY REPORT  #####

@app.route("/dailyreport",methods=['GET','POST'])
@login_required
def dailyreport():
    name=current_user.name
    form=Dailyreportform()
    return render_template('adddailyreport.html',name=name,form=form)



##### ADD DAILY REPORT #####


@app.route("/adddailyreport",methods=['GET','POST'])
@login_required
def adddailyreport():
    name=current_user.name
    form=Dailyreportform()
    if form.validate_on_submit():
        cp=form.buying_price.data
        sp=form.selling_price.data
        profit=sp-cp
        dailyreport=Dailyreport(item_name=form.item_name.data,buying_price=form.buying_price.data,selling_price=form.selling_price.data,profit_loss=profit,remarks=form.remarks.data)
        db.session.add(dailyreport)
        db.session.commit()
        flash('Record added successfully')
        return redirect(url_for('adddailyreport',name=name))
    else:
        print(form.errors)
    return render_template('adddailyreport.html',form=form,name=name)



##### VIEW DAILY REPORT #####


@app.route("/viewdailyreport",methods=['GET','POST'])
@login_required
def viewdailyreport():
    user_date=None
    form=Daybookform()
    name=current_user.name
    report=Dailyreport.query.all()
    return render_template('viewdailyreport.html',name=name,report=report,form=form,user_date=user_date)


##### DELETE DAILY REPORT #####

@app.route("/deletedailyreport/<int:id>",methods=['GET','POST'])
@login_required
def deletedailyreport(id):
    name=current_user.name
    report=Dailyreport.query.select_from(Dailyreport).filter_by(id=id).first()
    try:
        db.session.delete(report)
        db.session.commit()
        return redirect(url_for('viewdailyreport',name=name))
    except:
        flash("There was a problem deleting that record")
        return redirect(url_for('viewdailyreport',name=name))


######################################################################################################################


##### FILTER RECORD #####


@app.route("/filter",methods=['GET','POST'])
@login_required
def filter():
    name=current_user.name
    form=SearchForm()
    if form.validate_on_submit():
        mob_no=form.search.data
        result=services.query.filter_by(customer_mobile=mob_no).all()
        return render_template('filter.html',result=result,name=name,form=form)
    else:
        flash("No record found")
        print(form.errors)
        return redirect(url_for('viewrecord'))
    return render_template('filter.html',name=name,form=form)


##### VIEW/PRINT RECORD #####

@app.route("/view_print/<int:id>")
@login_required
def view_print(id):
    form=SearchForm()
    name=current_user.name
    service=services.query.select_from(services).filter_by(id=id).first()
    return render_template('view_print.html',service=service,name=name,form=form)


##### FILTER BY DATE FOR DAILY REPORTS #####

@app.route("/filter_daybook",methods=['GET','POST'])
def filter_daybook():
    form=Daybookform()
    if form.validate_on_submit():
        user_date=form.date.data
        report = Dailyreport.query.filter_by(date_added=user_date).all()
    return render_template('viewdailyreport.html',form=form, user_date=user_date,report=report)
    




######################################################################################################################







## DATABASE MODELS ##


class Users(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    username=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(150), nullable=False)
    mobile=db.Column(db.String(120),nullable=False)
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    password_hash=db.Column(db.String(128))


class services(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_name=db.Column(db.String(50),nullable=False)  #nullable=False means it is required
    customer_mobile=db.Column(db.String(50),nullable=False)  #nullable=False
    customer_email=db.Column(db.String(50),nullable=False)   #nullable=False
    customer_address=db.Column(db.String(50),nullable=False)  #,widget=TextArea())
    serial_no=db.Column(db.String(100),nullable=False)   #serial no of the product
    product_name=db.Column(db.String(200),nullable=False)  #product name
    service_type=db.Column(db.String(50),nullable=False)  #repair or service
    service_cost=db.Column(db.Integer,nullable=False)  #selling price of the product
    remarks=db.Column(db.String(200),nullable=True)  #remarks
    date_added=db.Column(db.Date, default=date.today)


class Dailyreport(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(50),nullable=False)
    buying_price=db.Column(db.Integer,nullable=False)  #buying price of the product
    selling_price=db.Column(db.Integer,nullable=False)  #selling price of the product
    profit_loss=db.Column(db.Integer,nullable=False)  #profit or loss
    remarks=db.Column(db.String(200),nullable=True)  #remarks
    date_added=db.Column(db.Date, default=date.today)



if __name__ == "__main__":
    app.run(debug=True)