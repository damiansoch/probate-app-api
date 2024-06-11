"""
Serializers for loan APIs
"""
from django.db import transaction
from rest_framework import serializers
from core.models import (Solicitor,
                         Agency,
                         ApplicationStatus,
                         Application,
                         User,
                         Estate,
                         Asset,
                         Expense,
                         Dispute)
from user.serializers import UserSerializer


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


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ('id',)


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('id',)


class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ('id',)


class EstateSerializer(serializers.ModelSerializer):
    asset_set = AssetSerializer(many=True)
    expense_set = ExpensesSerializer(many=True)
    dispute_set = DisputeSerializer(many=True)

    class Meta:
        model = Estate
        fields = ['id', 'application', 'asset_set', 'expense_set', 'dispute_set']
        read_only_fields = ('id',)

    def validate(self, attrs):
        try:
            serializers.ModelSerializer.validate(self, attrs)
        except serializers.ValidationError as e:
            print(e.args)
            raise e
        return attrs

    def create(self, validated_data):
        assets_data = validated_data.pop('asset_set')
        expenses_data = validated_data.pop('expense_set')
        disputes_data = validated_data.pop('dispute_set')

        estate = Estate.objects.create(**validated_data)

        for asset_data in assets_data:
            Asset.objects.create(estate=estate, **asset_data)

        for expense_data in expenses_data:
            Expense.objects.create(estate=estate, **expense_data)

        for dispute_data in disputes_data:
            Dispute.objects.create(estate=estate, **dispute_data)

        return estate


class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    agency = AgencySerializer(required=True)
    application_status = ApplicationStatusSerializer(required=True)
    lead_solicitor = SolicitorSerializer(required=True)

    class Meta:
        model = Application
        fields = ['id', 'amount', 'term', 'user', 'application_status', 'created_by', 'agency', 'lead_solicitor']
        read_only_fields = ('id', 'created_by', 'date_submitted')

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        agency_data = validated_data.pop('agency')
        lead_solicitor_data = validated_data.pop('lead_solicitor')
        application_status_data = validated_data.pop('application_status')

        user = None
        if user_data:
            user, _ = User.objects.get_or_create(defaults=user_data, username=user_data['username'])
        agency, _ = Agency.objects.get_or_create(defaults=agency_data, name=agency_data['name'])
        lead_solicitor, _ = Solicitor.objects.get_or_create(defaults=lead_solicitor_data,
                                                            first_name=lead_solicitor_data['first_name'],
                                                            last_name=lead_solicitor_data['last_name'])
        application_status, _ = ApplicationStatus.objects.get_or_create(defaults=application_status_data,
                                                                        name=application_status_data['name'])

        # Check if the lead_solicitor belongs to agency
        if lead_solicitor not in agency.solicitors.all():
            # Add lead_solicitor to agency
            agency.solicitors.add(lead_solicitor)

        application = Application.objects.create(user=user, agency=agency, lead_solicitor=lead_solicitor,
                                                 application_status=application_status, **validated_data)

        return application

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        agency_data = validated_data.pop('agency', None)
        lead_solicitor_data = validated_data.pop('lead_solicitor', None)
        application_status_data = validated_data.pop('application_status', None)

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        if agency_data:
            agency = instance.agency
            for attr, value in agency_data.items():
                setattr(agency, attr, value)
            agency.save()

            if lead_solicitor_data:
                lead_solicitor = instance.lead_solicitor
                if lead_solicitor not in agency.solicitors.all():
                    agency.solicitors.add(lead_solicitor)
                for attr, value in lead_solicitor_data.items():
                    setattr(lead_solicitor, attr, value)
                lead_solicitor.save()

        if application_status_data:
            application_status = instance.application_status
            for attr, value in application_status_data.items():
                setattr(application_status, attr, value)
            application_status.save()

        return super().update(instance, validated_data)


class ApplicationDetailSerializer(ApplicationSerializer):
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields
