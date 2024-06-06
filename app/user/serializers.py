"""Serializers for the User Api view"""

from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate, )
from django.utils.translation import gettext as _

from core.models import Team


def get_default_team():
    default_team, created = Team.objects.get_or_create(name="Default")
    return default_team


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""

    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), default=get_default_team)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'name', 'team', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('is_active', 'is_staff', 'is_superuser', 'team')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        password = validated_data.pop('password', None)
        team = validated_data.pop('team', None)

        if team is None:
            team = get_default_team()

        user = self.Meta.model(**validated_data)
        user.team = team
        user.set_password(password)
        # user is saved after password is set
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update a user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the User auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
