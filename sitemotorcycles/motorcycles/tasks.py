from io import StringIO

from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import csv


@shared_task
def send_mails(user, fav):
    user_email = user.email
    sending_mail = send_mail(
        'Тестовая рассылка',
        f'вы добавили {fav} в избранное',
        'hyshikryst@yandex.ru',
        [user_email],
        fail_silently=False,
    )
    print("Voila, Email Sent to " + user.first_name)
    return sending_mail


@shared_task
def send_notification(user, order):
    rows = [order]
    csvfile = StringIO()
    fieldnames = list(rows[0].keys())
    user_email = user.email

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    email = EmailMessage(
        'Subject',
        'Body',
        'hyshikryst@yandex.ru',
        [user_email],
    )
    email.attach('file.csv', csvfile.getvalue(), 'text/csv')
    email.send()
    # user_email = user.email
    # sending_mail = send_mail(
    #     'Новый заказ',
    #     f'вы сделали заказ {order}',
    #     'hyshikryst@yandex.ru',
    #     [user_email],
    #     fail_silently=False,
    # )
    # print("Voila, Email Sent to " + user.first_name)
    # return sending_mail
