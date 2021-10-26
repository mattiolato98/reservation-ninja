# reservation-ninja

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the source code of [Reservation-Ninja](https://reservation-ninja.herokuapp.com/).

## Why

This project comes from the idea of simplify the process of classrooms reservation in the University of Modena and Reggio Emilia (UNIMORE).

## How to use it

- Sign up to the platform available at *https://reservation-ninja.herokuapp.com*
- Create your weekly schedule, by entering your lessons timetable
- Let the tool work, every morning you'll find the link to the daily reservations

## Development configuration

If you wish to contribute to the development of **Reservation Ninja**, read this section about how to configure your local environment.

If you have any question regarding **Reservation Ninja**, you are welcome to write an issue.

### Files

To set up the project you have to create two files:

- `reservation_tool_base_folder/email_settings.py` :arrow_right: in order to send emails
- `crypto.txt` :arrow_right: in order to encrypt/decrypt fields with a symmetric key

#### email_settings.py

Set up `reservation_tool_base_folder/email_settings.py` as follows:

```python
EMAIL_HOST = 'your.host'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your.user'
EMAIL_HOST_PASSWORD = 'your-password'
```

#### crypto.txt

Set up `crypto.txt` with a secret key to use either for encryption and decryption of users third party credentials. The key should be generated using *Fernet*, like so:

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
```

You can then simply copy and paste it in the file.

### Environment variables

You should setup some environment variables (when you develop the software locally):

- `PYTHONUNBUFFERED = 1`
- `DEBUG = 1`
- `ADMIN_ENABLED = 1`
- `SECURE_SSL_REDIRECT = 0`
- `SESSION_COOKIE_SECURE = 0`
- `CSRF_COOKIE_SECURE = 0`

<br>

---

<br>

<p align="center">
  <img title="" src="static/img/ninja.png" alt="Ninja icon" width="100" data-align="center">
</p>
<p align="center"><i>Unleash the power of the ninja</i></p>
