from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions
from knox.auth import TokenAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomTokenAuthentication(TokenAuthentication):
    def validate_user(self, auth_token):
        if auth_token.user.is_active == False:
            raise exceptions.AuthenticationFailed(
                (
                    "Your account has been suspended please contact your company admin for more details"
                ),
                code="user_suspended",
            )
        return super().validate_user(auth_token)


class KnoxScheme(OpenApiAuthenticationExtension):
    target_class = "user_app.auth.CustomTokenAuthentication"
    name = "Knox Authorization"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
