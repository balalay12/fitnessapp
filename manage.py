from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.mod_auth.models import User

migrate = Migrate(app, db)

manager = Manager(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # $ python manage.py runserver
    # $ python manage.py db init
    # $ python manage.py db migrate
    # $ python manage.py db upgrade
    # $ python manage.py db --help
    manager.run()