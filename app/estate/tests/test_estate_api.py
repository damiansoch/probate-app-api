"""
Tests for etate api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Estate
from core.helper_estate_models import Asset, Dispute, Expense

from estate.serializers import (EstateSerializer, )


class PublicEstateAPITestCase(APITestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.SOLICITOR_URL = reverse('loan:estate-list')

    def test_login_required(self):
        """Test that login is required for retrieving estate list"""

        response = self.client.get(self.SOLICITOR_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEstateAPITestCase(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.SOLICITOR_URL = reverse('loan:estate-list')

    def test_retrieve_estate_list(self):
        """Test retrieving a list of estates including assets, expenses, and disputes"""

        estate1 = Estate.objects.create(

        )
        Asset.objects.create(
            name='Asset 1',
            estate=estate1
        )
        Expense.objects.create(
            name='Expense 1',
            estate=estate1
        )
        Dispute.objects.create(
            description='Dispute 1',
            estate=estate1
        )

        estate2 = Estate.objects.create(

        )
        Asset.objects.create(
            name='Asset 2',
            estate=estate2
        )
        Expense.objects.create(
            name='Expense 2',
            estate=estate2
        )
        Dispute.objects.create(
            description='Dispute 2',
            estate=estate2
        )

        res = self.client.get(self.SOLICITOR_URL)

        estates = Estate.objects.all().order_by('-id')
        serializer = EstateSerializer(estates, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
