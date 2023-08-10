
from application.jobs import workers
from application.jobs import tasks
from flask import Flask
from flask_restful import Api
import logging
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_security.utils import hash_password
from celery.schedules import crontab


from api.TestAPI import TestAPI
from api.VenueAPI import VenueAPI
from api.UserAPI import UserAPI
from api.LoginAPI import LoginAPI
from api.TestAuth import TestAUTHAPI
from api.ShowAPI import ShowAPI
from api.BookingAPI import BookingAPI


from application.security import user_datastore, sec
from application.db import db
from application.cache import cache
import application.config as config


app = Flask(__name__)
app.config.from_object(config)


# Enable Flask Cache
cache.init_app(app)
CORS(app)


# Flask Database Settings
migrate = Migrate(app, db)
db.init_app(app)

# Enable Celery
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    timezone = "Asia/kolkata",

)
celery.Task = workers.ContextTask

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("something supposed to happen")
    # sender.add_periodic_task(
    #     5,
    #     # crontab(minute=6, hour=1, day_of_month='*'),
    #                          tasks.sendDailyReminder.s(),
    #                          name='send example mail every 5 seconds')
    
    sender.add_periodic_task(
        5,
        # crontab(minute=6, hour=1, day_of_month='*'),
                             tasks.monthlyMail.s(),
                             name='send example mail every 5 seconds')
# Flask Logging
# logging.basicConfig(filename='cards.log', level=logging.INFO,
#     format='[%(asctime)s] %(levelname)s %(name)s in %(module)s: %(message)s')

jwt = JWTManager(app)

# Flask API
api = Api(app)
api.init_app(app)

# Flask Security
sec.init_app(app, user_datastore)

app.app_context().push()

def create_amdin():
    admin_role = user_datastore.find_or_create_role('admin')
    user_role = user_datastore.find_or_create_role('user')
    if not user_datastore.find_user(email='admin@example.com'):
        user_datastore.create_user(
        email='admin@example.com',
        password=hash_password('adminpassword'),
        roles=[admin_role]  # Assign the admin role to the user
        )
    db.session.commit()



api.add_resource(TestAPI, "/api/test/")
api.add_resource(VenueAPI, "/api/venue", "/api/venue/<int:id>")
api.add_resource(UserAPI, "/api/user", "/api/user/<int:id>")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(TestAUTHAPI, "/api/testauth")
api.add_resource(ShowAPI, "/api/show", "/api/show/<int:id>")
api.add_resource(BookingAPI, "/api/booking", "/api/booking/<int:id>")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_amdin()
        app.run(debug=True)


