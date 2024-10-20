from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Transaction
from .recurring import handle_recurring_transactions
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TransactionTests(APITestCase):
    """Tests for the Transaction model and its API."""

    def setUp(self):
        """Create a user for testing."""
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )
        self.transaction_data = {
            'amount': 100.00,
            'transaction_type': 'income',
            'category': 'Salary',
            'description': 'Monthly salary',
            'recurring': True,
            'recurrence_interval': 'monthly',
            'recurrence_end_date': '2024-12-31',
        }
        # Obtain a token for the user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Add the JWT token to the client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create an initial transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            **self.transaction_data
        )

    def test_create_transaction(self):
        """Test creating a new transaction."""
        response = self.client.post(
            reverse('transactions-list'), 
            self.transaction_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)  # Includes the one created in setUp

    def test_create_transaction_without_amount(self):
        """Test creating a transaction without amount fails."""
        data = self.transaction_data.copy()
        data['amount'] = 0  # Invalid amount
        response = self.client.post(
            reverse('transactions-list'), 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_transaction(self):
        """Test retrieving a transaction."""
        response = self.client.get(
            reverse('transactions-detail', args=[self.transaction.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.transaction.description)

    def test_update_transaction(self):
        """Test updating a transaction."""
        updated_data = {
            'amount': 150.00,
            'transaction_type': 'expense',
            'category': 'Food',
            'description': 'Grocery shopping',
            'recurring': False,
            'recurrence_interval': None,
            'recurrence_end_date': None,
        }
        response = self.client.put(
            reverse('transactions-detail', args=[self.transaction.id]),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 150.00)
        self.assertEqual(self.transaction.category, 'Food')

    def test_delete_transaction(self):
        """Test deleting a transaction."""
        response = self.client.delete(
            reverse('transactions-detail', args=[self.transaction.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_recurring_transaction_creation(self):
        """Test handling of recurring transactions."""
        # Set up a recurring transaction with a specific interval and future end date
        transaction = Transaction.objects.create(
            user=self.user,
            amount=100,
            transaction_type='income',  # Example transaction type
            category='Salary',  # Example category
            description='Monthly Salary',
            recurring=True,
            recurrence_interval='monthly',
            recurrence_end_date=timezone.now() + timedelta(days=30),  # Set end date in future
            last_occurrence_date=None  # Initializing last_occurrence_date
        )
    
        # Call the function that processes recurring transactions
        from .recurring import handle_recurring_transactions
        handle_recurring_transactions()

        # Verify that a new transaction has been created
        self.assertEqual(Transaction.objects.count(), 2)  # 1 original + 1 new

    def test_create_transaction_with_negative_amount(self):
        """Test creating a transaction with a negative amount fails."""
        data = self.transaction_data.copy()
        data['amount'] = -50.00  # Invalid amount
        response = self.client.post(
            reverse('transactions-list'), 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount must be greater than zero.", response.data['non_field_errors'])

