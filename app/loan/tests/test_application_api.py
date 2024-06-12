"""
Tests for application api
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import user
from core.models import (Application, ApplicationStatus, Agency, Solicitor, User, )

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

    def test_create_application_with_an_agency_and_lead_solicitor_returns_error(self):
        """Test for creating application with no agency and solicitor returns error"""
        application_status = ApplicationStatus.objects.create(name="Test Status")
        application_status_serializer = serializers.ApplicationStatusSerializer(application_status)
        payload = {
            "amount": "12345.67",
            "term": 12,
            "user": None,  # UserID here
            "application_status": application_status_serializer.data,  # ApplicationStatus ID here
            "agency": None,  # Agency ID here
            "lead_solicitor": None  # Solicitor ID here
        }
        res = self.client.post(self.APPLICATION_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST),

        # application = Application.objects.get(id=res.data['id'])
        # application.created_by = self.user
        # application.save()
        # application_serializer = serializers.ApplicationDetailSerializer(application)
        # self.assertEqual(res.data, application_serializer.data)

    def test_create_application_with_existing_agency_and_existing_solicitor(self):
        """Test for creating application with existing agency and existing solicitor"""
        application_status = ApplicationStatus.objects.create(name="Test Status")

        agency = Agency.objects.create(name="Test Agency",
                                       house_number=24,
                                       street="Test Street",
                                       town="Test town",
                                       county="Test county",
                                       eircode="d24n1f2")
        solicitor = Solicitor.objects.create(
            title="Mr",
            first_name="testName",
            last_name="TestLName",
            email="user@example.com",
            phone_number="0864567894",
            agency=agency
        )

        payload = {
            "amount": "12345.67",
            "term": 12,
            "application_status": application_status.id,  # ApplicationStatus ID here
            "agency": agency.id,
            "lead_solicitor": solicitor.id,
            "user": self.user.id,
        }

        res = self.client.post(self.APPLICATION_URL, payload, format='json')
        if res.status_code >= 400:
            print(res.json())
        application = Application.objects.get(id=res.data['id'])
        application.created_by = self.user
        application.save()
        agency = Agency.objects.all()
        solicitors = Solicitor.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        application_serializer = serializers.ApplicationDetailSerializer(Application.objects.get(id=res.data['id']))
        self.assertEqual(res.data, application_serializer.data)
        self.assertEqual(agency.count(), 1)
        self.assertEqual(agency[0].solicitors.count(), 1)
        self.assertEqual(solicitors.count(), 1)
        self.assertEqual(solicitors[0].agency.id, agency[0].id)

    def test_update_application(self):
        """Test for updating application"""

        application = create_loan_application_model(user=self.user)
        res = self.client.patch(detail_url(application.id), {'amount': "12345.67"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['amount'], "12345.67")

    def test_update_applications_agency_and_solicitor(self):
        application_status = ApplicationStatus.objects.create(name="Test Status")

        agency = Agency.objects.create(name="Test Agency",
                                       house_number=24,
                                       street="Test Street",
                                       town="Test town",
                                       county="Test county",
                                       eircode="d24n1f2"
                                       )
        solicitor = Solicitor.objects.create(title='Mr',
                                             first_name="TestName",
                                             last_name="TestLName",
                                             email="user@example.com",
                                             phone_number="0864567894",
                                             agency=agency
                                             )
        application = Application.objects.create(amount="350000",
                                                 term=12,
                                                 application_status=application_status,
                                                 agency=agency,
                                                 lead_solicitor=solicitor
                                                 )

        payload = {
            "agency": agency.id,
            "lead_solicitor": solicitor.id
        }

        response = self.client.patch(detail_url(application.id), payload, format='json')
        application.refresh_from_db()
        application_serializer = serializers.ApplicationDetailSerializer(application)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, application_serializer.data)

    def test_delete_application(self):
        """Test for deleting application"""
        application = create_loan_application_model(user=self.user)
        res = self.client.delete(detail_url(application.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.all().count(), 0)


class ApplicationDeletionTestCase(TestCase):
    def setUp(self):
        # Assuming we have User model available from Django auth system
        self.user = User.objects.create_user(name='testuser', password='12345', email="test@email.com")
        self.agency = Agency.objects.create(name='TestAgency', house_number='24')
        self.solicitor = Solicitor.objects.create(first_name='TestName', agency=self.agency, )
        self.application = Application.objects.create(user=self.user, agency=self.agency,
                                                      lead_solicitor=self.solicitor, term=12,
                                                      amount=1234.56)

    def test_delete_user(self):
        """Test that deletion of user assigned to an application is prevented"""
        with self.assertRaises(ProtectedError):
            self.user.delete()

    def test_delete_solicitor(self):
        """Test that deletion of lead solicitor assigned to an application is prevented"""
        with self.assertRaises(ProtectedError):
            self.solicitor.delete()
