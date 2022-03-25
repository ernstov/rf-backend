from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'confirm_password')
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                _("Password1 and Password2 should be same.")
            )

        if attrs["email"].split("@")[-1] not in settings.LIST_OF_ALLOWED_COMPANIES:
            raise serializers.ValidationError(_("Email domain not allowed"))
        return attrs

    def create(self, validated_data):
        """Method that creates new user"""
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        """Method that updates the user"""
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.set_password(validated_data["password"])
        instance.save()

        instance.refresh_from_db()

        return instance
