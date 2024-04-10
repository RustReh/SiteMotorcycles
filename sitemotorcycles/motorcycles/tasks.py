from celery import shared_task
from django.core.mail import send_mail


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
