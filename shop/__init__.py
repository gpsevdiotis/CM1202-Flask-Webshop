from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '09f5b852358a6227bf684de4e093dfebb78cd592f50a0564'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1945414:1qaz2wsx3edC@csmysql.cs.cf.ac.uk:3306/c1945414_Group14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes

from flask_admin import Admin
from shop.views import AdminView
from shop.models import User, Book
admin = Admin(app,name='Admin panel',template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Book, db.session))
