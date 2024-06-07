"""
Serializers for loan APIs
"""

from rest_framework import serializers
from core.models import (Solicitor, Agency, ApplicationStatus, Application)


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


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'
        read_only_fields = ('id',)


class AgencySerializer(serializers.ModelSerializer):
    solicitors = SolicitorSerializer(many=True, read_only=True)

    class Meta:
        model = Agency
        fields = '__all__'
        read_only_fields = ('id',)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'amount', 'term', 'user', 'application_status', 'created_by']
        read_only_fields = ('id', 'created_by', 'date_submitted')


class ApplicationDetailSerializer(ApplicationSerializer):
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields + ['agency', 'lead_solicitor']
