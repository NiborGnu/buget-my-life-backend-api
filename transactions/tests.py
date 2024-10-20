from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .recurring import handle_recurring_transactions
from .models import Transaction
from categories.models import Category
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TransactionTests(APITestCase):
    """Tests for the Transaction model and its API."""

    def setUp(self):
        """Set up the test user, categories, and transaction data."""
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

        # Create categories to be used in transactions
        self.income_category = Category.objects.create(
            name='Salary',
            category_type='income'
        )

        self.expense_category = Category.objects.create(
            name='Groceries',
            category_type='expense'
        )

        # Prepare transaction data
        self.transaction_data = {
            'amount': 100.00,
            'transaction_type': 'income',
            'category': self.income_category.id,
            'description': 'Monthly salary',
            'recurring': True,
            'recurrence_interval': 'monthly',
            'recurrence_end_date': '2024-12-31',
        }

        # Obtain a JWT token for the test user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Authenticate using the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create an initial transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=self.transaction_data['amount'],
            transaction_type=self.transaction_data['transaction_type'],
            category=self.income_category,  # Use income category for initial transaction
            description=self.transaction_data['description'],
            recurring=self.transaction_data['recurring'],
            recurrence_interval=self.transaction_data['recurrence_interval'],
            recurrence_end_date=self.transaction_data['recurrence_end_date'],
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
        """Test creating a transaction without a valid amount fails."""
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
            'category': self.expense_category.id,  # Ensure this is the expense category
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
        self.assertEqual(self.transaction.category.id, updated_data['category'])




    def test_delete_transaction(self):
        """Test deleting a transaction."""
        response = self.client.delete(
            reverse('transactions-detail', args=[self.transaction.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_recurring_transaction_creation(self):
        """Test the handling of recurring transactions."""
        # Set up a new recurring transaction
        recurring_transaction = Transaction.objects.create(
            user=self.user,
            amount=100.00,
            transaction_type='income',
            category=self.income_category,  # Ensure this is a valid income category
            description='Monthly Salary',
            recurring=True,
            recurrence_interval='monthly',
            recurrence_end_date=timezone.now() + timedelta(days=90),  # End date in 3 months
            last_occurrence_date=timezone.now() - timedelta(days=30),  # Last occurred 30 days ago
        )

        # Before calling the handler, check the initial count
        initial_count = Transaction.objects.count()

        # Call the recurring transaction handler
        handle_recurring_transactions()

        # Check the count of transactions after handling
        new_count = Transaction.objects.count()

        # Verify that a new transaction has been created
        self.assertEqual(new_count, initial_count + 1)  # Expecting one new transaction to be created


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
        self.assertIn("Amount must be greater than zero.", response.data['amount'])