from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PasswordChangeSerializer
from .serializers import SignInSerializer

User = get_user_model()


class SignInView(GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response({}, status=status.HTTP_202_ACCEPTED)


class PasswordChangeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({}, status=status.HTTP_202_ACCEPTED)


signin_view = SignInView.as_view()
signout_view = SignOutView.as_view()
password_change_view = PasswordChangeView.as_view()
