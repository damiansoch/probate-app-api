"""
Test for updating  dispute API
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Dispute
from loan.serializers import DisputeSerializer


def detail_url(dispute_id):
    """Return detail url for dispute detail view"""
    return reverse('loan:dispute-detail', args=[dispute_id])


class PublicDisputeAPITestCase(APITestCase):
    """test unauthenticated access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving disputes"""
        response = self.client.get(detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDisputeAPITestCase(APITestCase):
    """test authenticated access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_dispute_by_id(self):
        """Test retrieving dispute by id"""
        dispute = Dispute.objects.create(
            estate=None,
            description='test',
        )
        res = self.client.get(detail_url(dispute.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = DisputeSerializer(dispute)
        self.assertEqual(res.data, serializer.data)

    def test_update_dispute_by_id(self):
        """Test updating dispute by id"""
        dispute = Dispute.objects.create(
            estate=None,
            description='test',
        )
        data = {'description': 'test_updated'}
        url = detail_url(dispute.id)
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        dispute.refresh_from_db()
        self.assertEqual(dispute.description, data['description'])

    def test_delete_dispute_by_id(self):
        """Test deleting dispute by id"""
        dispute = Dispute.objects.create(
            estate=None,
            description='test',
        )
        res = self.client.delete(detail_url(dispute.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dispute.objects.count(), 0)
