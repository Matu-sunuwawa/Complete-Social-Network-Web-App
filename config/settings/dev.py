from .base import *

env = Env(DEBUG=(bool, True),SECRET_KEY=(str, 'django-insecure-dev-default-change-me'),)
env.read_env(BASE_DIR / ".env.dev")

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

DATABASES = {"default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337", "http://127.0.0.1:1337"]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
