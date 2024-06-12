"""
Tests for solicitor api
"""
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Solicitor, Agency

from loan.serializers import (SolicitorSerializer, )


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


def create_solicitor(**kwargs):
    """creates a new solicitor"""
    agency = create_agency_model()
    defaults = {
        "title": "Miss",
        "first_name": "Test",
        "last_name": "Solicitor",
        "email": "test@example.com",
        "phone_number": "0868455579",
        "agency": agency,
    }
    defaults.update(kwargs)
    return Solicitor.objects.create(**defaults)


# endregion

class PublicSolicitorAPITestCase(APITestCase):
    """Test unauthenticated access to SolicitorAPI"""

    def setUp(self):
        self.client = APIClient()
        self.SOLICITOR_URL = reverse('loan:solicitor-list')

    def test_login_required(self):
        """Test that login is required for retrieving solicitors"""
        response = self.client.get(self.SOLICITOR_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSolicitorAPITestCase(APITestCase):
    """Test authenticated access to SolicitorAPI"""

    def setUp(self):
        self.client = APIClient()
        self.SOLICITOR_URL = reverse('loan:solicitor-list')
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_solicitors(self):
        """Test retrieving a list of solicitors"""
        create_solicitor(email="test1@example.com")
        create_solicitor(email="test2@example.com")
        response = self.client.get(self.SOLICITOR_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        solicitors = Solicitor.objects.all().order_by('last_name')
        serializer = SolicitorSerializer(solicitors, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_solicitor_without_agency(self):
        """test creating a solicitor create solicitor without agency returns error"""

        solicitor_data = {
            "title": "Mr",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.SOLICITOR_URL, solicitor_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f'Expected status code {status.HTTP_400_BAD_REQUEST}, but got {response.status_code} with response {response.data}')

    def test_delete_solicitor(self):
        """Test deleting a solicitor"""

        solicitor = create_solicitor()
        response = self.client.delete(reverse('loan:solicitor-detail', args=[solicitor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_partial_update_solicitor(self):
        """Test partially updating a solicitor"""
        solicitor = create_solicitor()
        new_last_name = "New Last Name"
        response = self.client.patch(reverse('loan:solicitor-detail', args=[solicitor.id]),
                                     {'last_name': new_last_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], new_last_name)

    def test_full_update_solicitor(self):
        """Test updating a solicitor"""
        solicitor = create_solicitor()
        agency = create_agency_model()
        new_data = {
            "title": "Mrs",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone_number": "9876543210",
            "agency": agency.id,
        }
        response = self.client.put(reverse('loan:solicitor-detail', args=[solicitor.id]), new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_data['title'])
        self.assertEqual(response.data['first_name'], new_data['first_name'])
        self.assertEqual(response.data['last_name'], new_data['last_name'])
        self.assertEqual(response.data['email'], new_data['email'])
        self.assertEqual(response.data['phone_number'], new_data['phone_number'])

    def test_retrieve_solicitor_by_id(self):
        """Test retrieving a solicitor by id"""
        solicitor = create_solicitor()
        response = self.client.get(reverse('loan:solicitor-detail', args=[solicitor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SolicitorSerializer(solicitor)
        self.assertEqual(response.data, serializer.data)
