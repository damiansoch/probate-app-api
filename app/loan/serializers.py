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
    agency = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all())

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
        read_only_fields = ('id', 'estate')


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('id', 'estate')


class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ('id', 'estate')


class EstateSerializer(serializers.ModelSerializer):
    asset_set = AssetSerializer(many=True)
    expense_set = ExpensesSerializer(many=True)
    dispute_set = DisputeSerializer(many=True)

    class Meta:
        model = Estate
        fields = ['id', 'application', 'asset_set', 'expense_set', 'dispute_set']
        read_only_fields = ('id',)

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

    def validate(self, attrs):
        try:
            serializers.ModelSerializer.validate(self, attrs)
        except serializers.ValidationError as e:
            print(e.args)
            raise e
        return attrs


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, default=None)
    created_by = UserSerializer(read_only=True)
    agency = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all())
    application_status = serializers.PrimaryKeyRelatedField(queryset=ApplicationStatus.objects.all())
    lead_solicitor = serializers.PrimaryKeyRelatedField(queryset=Solicitor.objects.all())
    estate = EstateSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'amount', 'term', 'user', 'application_status', 'created_by', 'agency', 'lead_solicitor',
                  'estate']
        read_only_fields = ('id', 'created_by', 'date_submitted', 'estate')

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop('user', None)
        agency = validated_data.pop('agency', None)
        lead_solicitor = validated_data.pop('lead_solicitor')
        application_status_data = validated_data.pop('application_status', None)

        application = Application.objects.create(user=user, agency=agency, lead_solicitor=lead_solicitor,
                                                 application_status=application_status_data, **validated_data)

        return application

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Fetch 'user' data and update
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update 'agency' and 'application_status' with given IDs
        if 'agency' in validated_data:
            instance.agency_id = validated_data.pop('agency')
        if 'application_status' in validated_data:
            instance.application_status_id = validated_data.pop('application_status')

        # Update remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        estate = Estate.objects.filter(application=instance)
        # make sure it matches your related_name setting in the estate ForeignKey in your model,
        # if it's not specified, you can access it by lower cased, plural form of the model by default.

        if estate.exists():
            representation['estate'] = EstateSerializer(estate.first()).data
        else:
            representation['estate'] = None

        return representation


class ApplicationDetailSerializer(ApplicationSerializer):
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields
