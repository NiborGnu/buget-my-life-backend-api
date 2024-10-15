from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class UserModelTests(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.username = 'testuser'
        self.password = 'AstrongPassword123!'
        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.username, self.username)
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_superuser_creation(self):
        """Test that a superuser is created successfully."""
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superpassword123!'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class CustomRegisterSerializerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'AstrongPassword123!',  # Use a stronger password
            'password2': 'AstrongPassword123!'   # Match the passwords
        }
        self.invalid_payload = {
            'email': '',
            'username': '',
            'password1': 'AstrongPassword123!',
            'password2': 'differentpassword'
        }

    def test_register_user_success(self):
        """Test registering a new user with valid credentials."""
        response = self.client.post(reverse('rest_register'), self.valid_payload)
        print(response.data)  # Print response data for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'newuser@example.com')

    def test_register_user_invalid(self):
        """Test registering a new user with invalid credentials."""
        response = self.client.post(reverse('rest_register'), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_password_mismatch(self):
        """Test registering a new user with password mismatch."""
        payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'AstrongPassword123!',
            'password2': 'differentpassword'  # Different password
        }
        response = self.client.post(reverse('rest_register'), payload)
        print(response.data)  # Print response data for debugging
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)  # Ensure the error is in non_field_errors
