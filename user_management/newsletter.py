from django.core.mail import send_mail
from os.path import dirname

import django
import os
import sys

PROJECT_PATH = os.path.join(dirname(__file__), "../")


def send_newsletter(user):
    mail_subject = 'Che fine hai fatto?'

    send_mail(
        mail_subject,
        (
            f'''Ciao {user.username},\n'''
            + '''\nReservation Ninja è di nuovo online!\n'''
            + '''\nAccedi al tuo account per inserire gli orari del secondo semestre '''
            + '''e sfruttare le prenotazioni automatiche.\n'''
            + '''\nReservation Ninja'''
        ),
        'reservationtoolninja@gmail.com',
        [user.email],
        fail_silently=False,
    )

    print(f'{user.email} Sent email')


if __name__ == '__main__':
    # Django environment initialization:
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings")
    django.setup()

    from user_management.models import PlatformUser


    for u in PlatformUser.objects.filter(username='provaaa'):
        send_newsletter(u)