"""
Serializers for loan APIs
"""

from rest_framework import serializers, viewsets
from core.models import Solicitor


class SolicitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitor
        fields = '__all__'
        read_only_fields = ('id',)


class SolicitorViewSet(viewsets.ModelViewSet):
    queryset = Solicitor.objects.all().order_by('last_name')
    serializer_class = SolicitorSerializer
