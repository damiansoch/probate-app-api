"""
Views ro loan API
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loan import serializers
from core.models import (Solicitor, Agency)


class SolicitorViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for listing Solicitors"""
    serializer_class = serializers.SolicitorSerializer
    queryset = Solicitor.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.order_by('last_name')


class AgencyViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet for listing Agencies"""
    serializer_class = serializers.AgencySerializer
    queryset = Agency.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.order_by('name')
