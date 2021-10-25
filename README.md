# reservation-ninja

This is the source code of [Reservation-Ninja](https://reservation-ninja.herokuapp.com/).

## Configuration

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
Set up crypto.txt with a secret key to use either for encryption and decryption of users third party credentials. The key should be generated using *Fernet*, like so:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
```
You can then simply copy and paste it in the file.

### Environment variables
You should setup some environment variables:
  - `PYTHONUNBUFFERED = 1`
  - `DEBUG = 1`
  - `ADMIN_ENABLED = 1`
  - `SECURE_SSL_REDIRECT = 0`
  - `SESSION_COOKIE_SECURE = 0`
  - `CSRF_COOKIE_SECURE = 0`
