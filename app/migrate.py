from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.extensions import db

app = create_app('development')
migrate = Migrate(app, db)
migrate.init_app(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
