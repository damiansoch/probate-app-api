"""
Tests for models
"""
from datetime import datetime
import random
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from loan import serializers


# region<helper functions>
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
    return models.Agency.objects.create(**defaults)


# endregion


class TestModels(TestCase):
    """Tests for models"""

    # region <Tests fo User model>
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'testemail@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.COM", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user with no email is raised error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "sample123")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com", "testpass123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # endregion

    # region <Tests of all models>
    def test_create_solicitor(self):
        """Test creating a solicitor"""
        agency = create_agency_model()
        solicitor = models.Solicitor.objects.create(
            title="Mr",
            first_name="Test",
            last_name="Name",
            email="test@erxample.com",
            phone_number="1234567890",
            agency=agency
        )
        self.assertEqual(str(solicitor), f"{solicitor.title} {solicitor.first_name} {solicitor.last_name}")

    def test_create_agency(self):
        """Test creating an agency"""
        agency = models.Agency.objects.create(
            name="Test Agency",
            house_number=random.randint(1, 200),
            street="Test Street",
            town="Test Town",
            county="Test County",
            eircode="1234567G",
        )
        self.assertEqual(str(agency), agency.name)

    def test_create_application(self):
        """Test creating an application"""
        application_status = models.ApplicationStatus.objects.create(name="Test Status")
        user = get_user_model().objects.create_user(email="test@example.com", password="testpass123")

        application = models.Application.objects.create(
            amount=Decimal("350_000"),
            term=24,
            user=None,
            application_status=application_status,
            agency=None,
            created_by=user,
            lead_solicitor=None,
        )

        self.assertEqual(application_status.name, "Test Status")
        self.assertEqual(application.amount, Decimal('350000'))
        self.assertEqual(application.term, 24)
    # endregion
