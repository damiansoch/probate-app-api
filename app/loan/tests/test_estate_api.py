"""
tests for estate api
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Estate, Application, ApplicationStatus, Agency, Solicitor, Asset, Expense, Dispute

from loan.serializers import (EstateSerializer, ApplicationSerializer, )


def detail_url(estate_id):
    """Return detail url for a given estate"""
    return reverse('loan:estate-detail', args=[estate_id])


def create_application():
    application_status = ApplicationStatus.objects.create(name="Test Status")
    agency = Agency.objects.create(name="Test Agency")
    solicitor = Solicitor.objects.create(
        title="Mr",
        first_name="Test",
        last_name="Name",
        email="test@erxample.com",
        phone_number="1234567890",
        agency=agency
    )
    application = Application.objects.create(
        amount="350000",
        term=12,
        application_status=application_status,
        agency=agency,
        lead_solicitor=solicitor,

    )
    return application


class PublicEstateAPITestCase(APITestCase):
    """Test the unauthenticated Estate API requests"""

    def setUp(self):
        self.client = APIClient()
        self.ESTATES_URL = reverse('loan:estate-list')

    def test_login_required(self):
        """Test that login is required for retrieving Estate"""
        response = self.client.get(self.ESTATES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEstateAPITestCase(APITestCase):
    """Test the authenticated Estate API requests"""

    def setUp(self):
        self.client = APIClient()
        self.ESTATES_URL = reverse('loan:estate-list')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_Estate_list(self):
        """Test retrieving a list of Estate"""
        application = create_application()
        estate1 = Estate.objects.create(application=application)
        estate2 = Estate.objects.create(application=application)

        response = self.client.get(self.ESTATES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        estates = Estate.objects.all().order_by('-id')
        serializer = EstateSerializer(estates, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_Estate_with_assets_expenses_and_dispute(self):
        """Test creating a new Estate"""
        application = create_application()

        data = {
            'application': application.id,
            'asset_set': [
                {'section': 'Test Section',
                 'title': 'Asset Title',
                 'description': 'Asset Description',
                 'value': 100.0
                 },

            ],
            'expense_set': [
                {'section': 'Test Section',
                 'title': 'Expense Title',
                 'description': 'Expense Description',
                 'value': 100.0
                 },

            ],
            'dispute_set': [
                {'description': 'Dispute Description'},

            ]
        }

        response = self.client.post(self.ESTATES_URL, data, format='json')
        response_status = response.status_code
        response_data = response.data
        self.assertEqual(response_status, status.HTTP_201_CREATED,
                         f'Expected response status code: {status.HTTP_201_CREATED}, but got: {response_status} {response_data}')
        estate = Estate.objects.get(id=response.data['id'])
        serializer = EstateSerializer(estate)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response_data["application"], application.id)

    def test_retrieve_Estate_by_id(self):
        """Test retrieving the Estate by id"""
        estate = Estate.objects.create(application=create_application())
        response = self.client.get(detail_url(estate.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        estate = Estate.objects.get(id=estate.id)
        serializer = EstateSerializer(estate)
        self.assertEqual(response.data, serializer.data)

    def test_delete_Estate(self):
        """Test deleting an Estate"""
        estate = Estate.objects.create(application=create_application())
        response = self.client.delete(detail_url(estate.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Estate.objects.filter(id=estate.id).exists())

    def test_delete_estate_deletes_assets_expenses_and_disputes_for_this_estate(self):
        """Test deleting an Estate together with all data"""
        estate = Estate.objects.create(application=create_application())
        estate.asset_set.create(
            section='Test Section',
            title='Asset Title',
            description='Asset Description',
            value=100.0
        )
        estate.expense_set.create(
            section='Test Section',
            title='Expense Title',
            description='Expense Description',
            value=100.0
        )
        estate.dispute_set.create(
            description='Dispute Description'
        )
        response = self.client.delete(detail_url(estate.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Estate.objects.filter(id=estate.id).exists())
        self.assertFalse(Asset.objects.filter(estate=estate).exists())
        self.assertFalse(Expense.objects.filter(estate=estate).exists())
        self.assertFalse(Dispute.objects.filter(estate=estate).exists())
