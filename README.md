# reservation-ninja

This is the source code of [Reservation-Ninja](https://reservation-ninja.herokuapp.com/).

## Configuration

### Files

To set up the project you have to create two files:
  - `reservation_tool_base_folder/email_settings.py` :arrow_right: in order to send emails
  - `crypto.txt` :arrow_right: in order to encrypt/decrypt fields with a symmetric key

#### Email settings
  
### Environment variables
  - `PYTHONUNBUFFERED = 1`
  - `DEBUG = 1`
  - `ADMIN_ENABLED = 1`
  - `SECURE_SSL_REDIRECT = 0`
  - `SESSION_COOKIE_SECURE = 0`
  - `CSRF_COOKIE_SECURE = 0`

...