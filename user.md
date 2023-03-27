## rest_framework install

#### 1 - install packages

        1) restframework
                pip install djangorestframework
                pip install markdown # Markdown support for the browsable API.
                pip install django-filter # Filtering support

                INSTALLED_APPS = [
                'rest_framework',
                "rest_framework.authtoken",
                ]

                REST_FRAMEWORK = () setting.py

        2) drf_spectacular swagger
                $ pip install drf-spectacular
                INSTALLED_APPS
                REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS":...} in setting.py
                urls

        3) Djoser (base token) to use knox
                $ pip install -U djoser
                INSTALLED_APPS =  'djoser'
                DJOSER = {
                        user:
                        user_create:
                        ......
                } setting.py

        4) knox login/logout/logout_all
                pip install django-rest-knox
                INSTALLED_APPS = 'knox'
                REST_KNOX = {
                        "USER_SERIALIZER": "user_app.serializers.UserSerializers",
                        "TOKEN_TTL": timedelta(hours=48),
                        } # what will raise in json API
                REST_FRAMEWORK = {DEFAULT_AUTH : user_app.auth.CustomTokenAuthentication}
                migrate

### 2 - adding user

        make USER & REGISTER
                - python manage.py startapp app_user
                - adding in INSTALLED_APPS
                - link the urls in core app
                - create user model and his managers
                - AUTH_USER_MODEL = "user_app.User" in setting.py
                - create CustomUserSerializers inherit from djoser (UserSerializer) # for user
                - create CreateUserSerializers inherit from djoser (UserCreateSerializer) # for create user
                - DOSER SERIALIZERS in setting.py (user/create_user/...)
                - you can override create method == register to change register serializer
                - put this serializer in view and make url for (get user / register)
                - admin.py
                - migrations & migrate user_app


        login Djoser & knox
                - create serializer inherit from (TokenCreateSerializer > from Djoser.serializers)
                - put authenticate user in attrs in def validate():

                # ---------- "Authentication knox.auth" in knox documentation ---------- #
                # view.py
                - create your LoginView inherit from (TokenCreateView > from Djoser.views) (LoginView > from knox.views)
                - take the use from serializer.validated_data then login and send it with request
                # urls.py
                from knox.views import LogoutAllView, LogoutView
                from user_app.views import LoginView
