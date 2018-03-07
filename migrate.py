from model import *
from ws import *

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.run()

#Commands for the terminal

#Only the fist time.
#python migrate.py db init -> Create folder migration

#Every time that you change the database structure
#python migrate.py db migrate -> Detection of all changes of your structure database and generate the version file.
#python migrate.py db upgrade -> Execute the version file, upgrade the database structure