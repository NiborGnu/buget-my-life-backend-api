from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import User
from rest_framework import serializers
from .serializers import CustomRegisterSerializer
from unittest.mock import Mock
from rest_framework.exceptions import ErrorDetail


class UserManagerTests(TestCase):
    
    def setUp(self):
        self.email = 'test@example.com'
        self.username = 'testuser'
        self.password = 'testpassword123'
    
    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superpassword123'
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertEqual(superuser.username, 'superuser')
        self.assertTrue(superuser.check_password('superpassword123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email='',
                username=self.username,
                password=self.password
            )
        self.assertEqual(str(context.exception), "The Email field must be set")
    
    def test_create_user_without_username(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email=self.email,
                username='',
                password=self.password
            )
        self.assertEqual(str(context.exception), "The Username field must be set")
    
    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email='invalidsuper@example.com',
                username='invalidsuperuser',
                password='superpassword123',
                is_staff=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')
    
    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email='invalidsuper@example.com',
                username='invalidsuperuser',
                password='superpassword123',
                is_superuser=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')

    def test_user_string_representation(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertEqual(str(user), self.email)

    def test_user_active_status_default(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertTrue(user.is_active)

    def test_user_staff_status_default(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertFalse(user.is_staff)

    def test_superuser_attributes(self):
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superpassword123'
        )
        self.assertTrue(superuser.is_active)

    def test_password_hashing(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.assertNotEqual(user.password, self.password)

    def test_user_creation_with_extra_fields(self):
        user = User.objects.create_user(
            email='extra@example.com',
            username='extratest',
            password='extratestpassword'
        )
        user.first_name = 'Extra'
        user.last_name = 'User'
        user.save()
        self.assertEqual(user.first_name, 'Extra')
        self.assertEqual(user.last_name, 'User')

    def test_email_uniqueness(self):
        User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.email,
                username='anotheruser',
                password='password123'
            )

    def test_username_uniqueness(self):
        User.objects.create_user(
            email='unique@example.com',
            username=self.username,
            password=self.password
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='anotherunique@example.com',
                username=self.username,
                password='password123'
            )


class CustomRegisterSerializerTests(TestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.mock_request = Mock()
        self.mock_request.session = {} 

    def test_register_user_success(self):
        serializer = CustomRegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save(self.mock_request)
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())

    def test_register_user_duplicate_email(self):
        User.objects.create_user(
            email=self.valid_data['email'],
            username='otheruser',
            password='password123'
        )
        serializer = CustomRegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'], ['This field must be unique.'])

    def test_register_user_duplicate_username(self):
        User.objects.create_user(
            email='other@example.com',
            username=self.valid_data['username'],
            password='password123'
        )
        serializer = CustomRegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertEqual(serializer.errors['username'], ['This field must be unique.'])

    def test_register_user_missing_email(self):
        data = self.valid_data.copy()
        data['email'] = ''
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_register_user_missing_username(self):
        data = self.valid_data.copy()
        data['username'] = ''
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_register_user_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword'
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'],
            [ErrorDetail(string="The two password fields didn't match.", code='invalid')])


class EdgeCaseTests(TestCase):

    def test_register_user_empty_email(self):
        data = {
            'email': '',
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'], ['This field may not be blank.'])

    def test_register_user_empty_username(self):
        data = {
            'email': 'test@example.com',
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertEqual(serializer.errors['username'], ['This field may not be blank.'])
