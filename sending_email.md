# setup celery with django and redis

## packages (set in INSTALLED_APPS)

    1- pip install celery
    2- pip install django-celery-beat

## commands to run celery

    # first run server

    # second in cmd to run worker that do the tasks
        celery -A djcelery_proj.celery worker --pool=solo -l info

## ----------------------------------------------------------------------------------------------------------

## project core app

##### 1- setting.py

    CELERY_BROKER_URL = "redis://127.0.0.1:6379" # redis end_point
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_TIMEZONE = "Africa/Cairo"

    CELERY_RESULT_BACKEND = "django-db"


    # ----------- SMTP ----------#
    # ----------- django email sitting ----------#
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "sending account"                # come from your google account
    EMAIL_HOST_PASSWORD = "google password"         # come from your (1-"google account manager" 2-"security" 3- 2step verfication 4-"apps passwords")
    DEFAULT_FROM_EMAIL = "default from email"

##### 2- **init**.py

    from .celery import app as celery_app
    __all__ = ("celery_app",)

##### 3- celery.py

        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery
        from django.conf import settings

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
        app = Celery("project_name")
        app.conf.update(timezone="Africa/Cairo")

        app.config_from_object(settings, namespace="CELERY")

# -----------------------------------------------------------------------

### send_mail app

##### 1 - tasks.py

    create your task that will run in the back_ground in this case sending email

##### 2 - views.py where do you want to do the task

    from sending_mail.tasks import payment_succeed_mail


    ...
    payment_succeed_mail.delay()  " to run the task here "
    ...
