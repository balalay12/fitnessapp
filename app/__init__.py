from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login_manager = LoginManager()

app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)


from app.mod_auth.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from app.mod_auth.views import mod_auth as auth_module
from app.mod_api.views import mod_api as api_module


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


app.register_blueprint(auth_module)
app.register_blueprint(api_module)

db.create_all()