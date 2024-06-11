"""
Test for updating assets, expense, and dispute APIs
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Asset


def detail_url(asset_id):
    """Return detail url for a given asset id"""
    return reverse('loan:asset-detail', args=[asset_id])


class PublicAssetAPITestCase(APITestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving assets"""
        response = self.client.get(detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAssetAPITestCase(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_asset_by_id(self):
        """Test retrieving asset by id"""
        asset = Asset.objects.create(
            section='Test Section',
            title="Test title",
            description="Test description",
            value=Decimal('10.00'),
            estate=None
        )
        url = detail_url(asset.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_asset_by_id(self):
        """Test updating asset by id"""
        asset = Asset.objects.create(
            section='Test Section',
            title="Test title",
            description="Test description",
            value=Decimal('10.00'),
            estate=None
        )
        data = {
            'section': 'Updated Section',
            'title': 'Updated Title',
            'description': 'Updated Description',
            'value': Decimal('20.00')
        }
        url = detail_url(asset.id)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error message {response.data}")
        asset.refresh_from_db()
        self.assertEqual(asset.section, data['section'])
        self.assertEqual(asset.title, data['title'])
        self.assertEqual(asset.description, data['description'])
        self.assertEqual(asset.value, data['value'])

    def test_delete_asset_by_id(self):
        """Test deleting asset by id"""
        asset = Asset.objects.create(
            section='Test Section',
            title="Test title",
            description="Test description",
            value=Decimal('10.00'),
            estate=None
        )
        response = self.client.delete(detail_url(asset.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Asset.objects.count(), 0)
