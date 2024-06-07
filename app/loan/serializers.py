"""
Serializers for loan APIs
"""

from rest_framework import serializers
from core.models import Solicitor, Agency


class AgencyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name']


class SolicitorSerializer(serializers.ModelSerializer):
    agency = AgencyNameSerializer(read_only=True)

    class Meta:
        model = Solicitor
        fields = '__all__'
        read_only_fields = ('id',)


class AgencySerializer(serializers.ModelSerializer):
    solicitors = SolicitorSerializer(many=True, read_only=True)

    class Meta:
        model = Agency
        fields = '__all__'
        read_only_fields = ('id',)
