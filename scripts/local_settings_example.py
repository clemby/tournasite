DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/database.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = ['localhost']

ADMINS = (
)

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'a terrible secret key! consider using a better one'
