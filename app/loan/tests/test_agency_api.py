"""
Tests for agency api
"""
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Agency

from loan.serializers import AgencySerializer


# region<helper functions>
def create_user(email="user@example.com", password="testpass123"):
    """Create and return a test user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


def create_agency_model(**params):
    defaults = {
        "name": "test agency",
        "house_number": str(random.randint(1, 200)),
        "street": "Test Street",
        "town": "Test Town",
        "county": "Dublin",
        "eircode": "D24N1F1",
    }
    defaults.update(params)
    return Agency.objects.create(**defaults)


# endregion

class PublicAgencyAPITestCase(APITestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving agencies"""
        url = reverse('loan:agency-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAgencyAPITestCase(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_agencies(self):
        """Test retrieving a list of agencies"""
        agency1 = create_agency_model()
        agency2 = create_agency_model(name="test agency2")
        url = reverse('loan:agency-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response_names = [agency['name'] for agency in response.data]
        self.assertIn(agency1.name, response_names)
        self.assertIn(agency2.name, response_names)

    def test_create_new_agency(self):
        """Test creating a new agency"""
        data = {
            "name": "New Agency",
            "house_number": "123",
            "street": "New Street",
            "town": "New Town",
            "county": "New County",
            "eircode": "D24N1F1",
        }
        response = self.client.post(reverse('loan:agency-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        agency = Agency.objects.get(id=response.data['id'])
        serializer = AgencySerializer(agency)
        self.assertEqual(serializer.data, response.data)

    def test_delete_agency(self):
        """Test deleting an existing agency"""
        agency = create_agency_model()
        url = reverse('loan:agency-detail', args=[agency.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Agency.objects.filter(id=agency.id).exists())

    def test_partial_update_agency(self):
        """Test updating an existing agency"""
        agency = create_agency_model()
        url = reverse('loan:agency-detail', args=[agency.id])
        data = {
            "name": "Updated Agency",
            "house_number": "456",
            "street": "Updated Street",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agency.refresh_from_db()
        serializer = AgencySerializer(agency)
        self.assertEqual(serializer.data, response.data)

    def test_full_update_agency(self):
        """Test updating an existing agency"""
        agency = create_agency_model()
        url = reverse('loan:agency-detail', args=[agency.id])
        data = {
            "name": "Updated Agency",
            "house_number": "456",
            "street": "Updated Street",
            "town": "Updated Town",
            "county": "Updated County",
            "eircode": "D24N1F1",
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agency.refresh_from_db()
        serializer = AgencySerializer(agency)
        self.assertEqual(serializer.data, response.data)

    def test_retrieve_agency_by_id(self):
        """Test retrieving a specific agency"""
        agency = create_agency_model()
        url = reverse('loan:agency-detail', args=[agency.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = AgencySerializer(agency)
        self.assertEqual(serializer.data, response.data)
