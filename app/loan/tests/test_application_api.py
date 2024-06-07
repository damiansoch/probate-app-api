"""
Tests for application api
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Application, ApplicationStatus

from loan import serializers
from user.serializers import UserSerializer


# region<helper functions>

def detail_url(application_id):
    """Create and returns a recipe detail URL"""
    return reverse('loan:application-detail', args=[application_id])


def create_user(**params):
    defaults = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    defaults.update(params)
    """Create and return a test user"""
    return get_user_model().objects.create_user(
        email=defaults["email"],
        password=defaults["password"]
    )


def create_loan_application_model(user, **params):
    application_status = ApplicationStatus.objects.create(name="Test Status")

    application = Application.objects.create(
        amount=Decimal("350_000"),
        term=24,
        user=None,
        application_status=application_status,
        agency=None,
        created_by=user,
        lead_solicitor=None,
    )
    return application


# endregion

class PublicApplicationApiTestCase(APITestCase):
    """Tests for public application api"""

    def setUp(self):
        self.client = APIClient()
        self.APPLICATION_URL = reverse('loan:application-list')

    def test_login_required(self):
        """Test that login is required for retrieving an application"""
        response = self.client.get(self.APPLICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApplicationApiTestCase(APITestCase):
    """Tests for private application api"""

    def setUp(self):
        self.client = APIClient()
        self.APPLICATION_URL = reverse('loan:application-list')
        self.user = create_user(email='test1@example.com')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_application_list(self):
        """Test retrieving a list of applications"""
        create_loan_application_model(user=self.user)
        create_loan_application_model(user=self.user, amount=Decimal("300_000"), term=12)

        response = self.client.get(self.APPLICATION_URL)
        applications = Application.objects.all().order_by('-id')
        serializer = serializers.ApplicationSerializer(applications, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serializer.data)

    def test_get_application_detail(self):
        """Test get recipe detail"""

        application = create_loan_application_model(user=self.user)
        url = detail_url(application.id)
        response = self.client.get(url)
        serializer = serializers.ApplicationDetailSerializer(application)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_application(self):
        """Test for creating application"""
        application_status = ApplicationStatus.objects.create(name="Test Status")
        payload = {
            "amount": "12345.67",
            "term": 12,
            "user": None,  # UserID here
            "application_status": application_status.id,  # ApplicationStatus ID here
            "agency": None,  # Agency ID here
            "lead_solicitor": None  # Solicitor ID here
        }
        res = self.client.post(self.APPLICATION_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        application = Application.objects.get(id=res.data['id'])
        application_serializer = serializers.ApplicationDetailSerializer(application)
        self.assertEqual(res.data, application_serializer.data)

    def test_update_application(self):
        """Test for updating application"""

        application = create_loan_application_model(user=self.user)
        res = self.client.patch(detail_url(application.id), {'amount': "12345.67"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['amount'], "12345.67")

    def test_delete_application(self):
        """Test for deleting application"""
        application = create_loan_application_model(user=self.user)
        res = self.client.delete(detail_url(application.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.all().count(), 0)
