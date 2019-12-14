from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotAuthenticated

User = get_user_model()


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField(label='Email', required=True)
    password = serializers.CharField(label='Password', required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        request = self.context.get('request')
        if email and password:
            user = authenticate(
                request=request,
                email=email,
                password=password
            )
            if not user:
                raise AuthenticationFailed()
        else:
            raise NotAuthenticated()

        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label='Old password', required=True)
    new_password = serializers.CharField(label='New password', required=True)
