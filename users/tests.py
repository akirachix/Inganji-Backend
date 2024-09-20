from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserProfileModelTest(TestCase):
    
    def setUp(self):
        self.UserProfile = get_user_model()

    def test_create_user_profile_happy_path(self):
        """Test creating a UserProfile with valid data."""
        user = self.UserProfile.objects.create_user(
            username='testuser',
            password='password123',
            role='admin'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'admin')
        self.assertTrue(user.check_password('password123'))

    def test_create_user_profile_unhappy_path_invalid_role(self):
        """Test creating a UserProfile with an invalid role."""
        with self.assertRaises(ValidationError):
            user = self.UserProfile(
                username='testuser_invalid',
                password='password123',
                role='invalid_role'
            )
            user.full_clean()  # This should raise a ValidationError

    def test_create_user_profile_unhappy_path_missing_role(self):
        """Test creating a UserProfile without specifying a role."""
        user = self.UserProfile(
            username='testuser_no_role',
            password='password123'
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # This should raise a ValidationError

    def test_create_user_profile_unhappy_path_no_username(self):
        """Test creating a UserProfile without a username."""
        user = self.UserProfile(
            password='password123',
            role='admin'
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # This should raise a ValidationError

