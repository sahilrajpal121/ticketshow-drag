from .workers import celery
from flask import current_app as app, url_for
from jinja2 import Template
from application.db import db, User, Booking 
from celery.schedules import crontab
from application.access import acs_user_all
from application.message import dailyRemainderEmail, mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from sqlalchemy import func

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # sender.add_periodic_task(
#     #     crontab(day_of_month=1, month_of_year='*'),
#     #     monthlyMail.s(),
#     # )
#     # sender.add_periodic_task(
#     #     crontab(minute=0, hour=18, day_of_month='*'),
#     #     dailyRemainder.s(),
#     # )
#     print("something supposed to happen")
#     sender.add_periodic_task(20,
#                              send_example_mail.s(),
#                              name='send example mail every 5 seconds')

# def send_email(to_address, subject, message):
#     msg = MIMEMultipart()
#     msg['From'] = "email@sahil.com"
#     msg['To'] = to_address
#     msg['Subject'] = subject

#     msg.attach(MIMEText(message, 'html'))

#     # s = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
#     # s.login(SENDER_ADDRESS, SENDER_PASSWORD)
#     s = smtplib.SMTP('127.0.0.1', 1025)
#     s.login("email@sahil.com", "password")
#     s.send_message(msg)
#     s.quit()

#     return True


@celery.task()
def sendDailyReminder():
    print('sending example mail')
    # for each user_id, get the user email
    # send email to each user
    all_users = User.query.with_entities(User.id, User.email).all()
    id_email = {user.id: user.email for user in all_users}
    all_user_id = set([user.id for user in all_users])
    # print(all_users)
    # print(all_user_id)
    # filter all the user_id who have booked today
    today = datetime.date.today()
    booked_today = Booking.query.filter(func.date(Booking.time) == today).with_entities(Booking.user_id).all()
    print("booked today", set(*booked_today), type(booked_today), booked_today)
    booked_today = set(*booked_today)
    # filter all the user_id who have not booked today
    not_booked_today = all_user_id - booked_today
    print("not booked today", not_booked_today)
    
    # send email to all the user_id who have not booked today
    for user_id in not_booked_today:
        print("sending email to", id_email[user_id])
        dailyRemainderEmail(id_email[user_id])

@celery.task()
def sendMonthlyMail(id, email):
    bookings = Booking.query.filter_by(user_id=id).with_entities(Booking.show_id, Booking.num_seats).all()
    bookings_seats = [booking.num_seats for booking in bookings]
    no_of_bookings = len(bookings_seats)
    sum_of_bookings = sum(bookings_seats)
    no_of_shows = len(set([booking.show_id for booking in bookings]))
    

    with open(f'{app.config["EMAIL_TEMPLATE"]}report.mail.html') as file:
        template = Template(file.read())
        message = template.render(email=email, no_of_bookings=no_of_bookings, sum_of_bookings=sum_of_bookings, no_of_shows=no_of_shows)

    mail(email, 'Monthly Review Report', message)

    return 'Sent Mail'


@celery.task()
def monthlyMail():
    users = acs_user_all()
    
    for user in users:
        sendMonthlyMail.delay(user.id, user.email)

    return 'Monthly Mail Sent'

@celery.task()
def test():
    print('RUNNING TEST')