from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.validated_data["user"])

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
