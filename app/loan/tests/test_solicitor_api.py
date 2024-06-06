"""
Tests for solicitor api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Solicitor

from loan.serializers import SolicitorSerializer


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a test user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


def create_solicitor(**kwargs):
    """creates a new solicitor"""
    defaults = {
        "title": "Miss",
        "first_name": "Test",
        "last_name": "Solicitor",
        "email": "test@example.com",
        "phone_number": "0868455579"
    }
    defaults.update(kwargs)
    return Solicitor.objects.create(**defaults)


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
