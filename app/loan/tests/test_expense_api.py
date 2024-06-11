from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Expense


def detail_url(expense_id):
    """Return detail url for a given expense id"""
    return reverse('loan:expense-detail', args=[expense_id])


class PublicExpenseAPITestCase(APITestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving expenses"""
        response = self.client.get(detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExpenseAPITestCase(APITestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_expense_by_id(self):
        """Test retrieving expense by id"""
        expense = Expense.objects.create(
            section='Test Section',
            title='Asset Title',
            description='Asset Description',
            value=100.0
        )
        url = detail_url(expense.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense_by_id(self):
        """Test updating expense by id"""
        expense = Expense.objects.create(
            section='Test Section',
            title='Asset Title',
            description='Asset Description',
            value=100.0
        )
        data = {
            'section': 'Updated Section',
            'title': 'Updated Title',
            'description': 'Updated Description',
            'value': Decimal('20.00')
        }
        url = detail_url(expense.id)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error message {response.data}")
        expense.refresh_from_db()
        self.assertEqual(expense.section, data['section'])
        self.assertEqual(expense.title, data['title'])
        self.assertEqual(expense.description, data['description'])
        self.assertEqual(expense.value, data['value'])

    def test_delete_expense_by_id(self):
        """Test deleting expense by id"""

        expense = Expense.objects.create(
            section='Test Section',
            title='Asset Title',
            description='Asset Description',
            value=100.0
        )

        response = self.client.delete(detail_url(expense.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
