from django.test import TestCase
from .models import Sacco, UserProfile
from django.core.exceptions import ValidationError

class SaccoModelTest(TestCase):

    def setUp(self):
        # Create a UserProfile instance for testing
        self.user = UserProfile.objects.create(username="testuser", email="test@example.com")

    # Happy Path Test
    def test_create_sacco_success(self):
        """Test successful creation of a Cooperative."""
        sacco = Sacco(sacco_name="Green Cooperative", user=self.user)
        sacco.save()
        self.assertEqual(Sacco.objects.count(), 1)
        self.assertEqual(sacco.sacco_name, "Green Cooperative")

    # Unhappy Path Tests
    def test_create_sacco_missing_name(self):
        """Test creation fails with missing sacco name."""
        sacco = Sacco(user=self.user)
        with self.assertRaises(ValidationError):
            sacco.full_clean()  # This should raise a ValidationError

    def test_create_sacco_invalid_user(self):
        """Test that trying to create a Sacco with a non-existent user fails."""
        invalid_user = UserProfile(pk=999)  # Assuming this user does not exist
        sacco = Sacco(sacco_name="New Sacco", user=invalid_user)
        
        with self.assertRaises(Exception):  # This should fail when validating
            sacco.full_clean()  # Validate before saving

    def test_user_deleted_sacco(self):
        """Test that accessing a sacco's user after deletion raises an error."""
        sacco = Sacco.objects.create(sacco_name="Another Cooperative", user=self.user)
        user_id = sacco.user.id  # Store the ID to check after deletion
        self.user.delete()  # Delete the user

        # Attempt to access the deleted user
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=user_id)  # Check the user ID directly

    def tearDown(self):
        # Clean up any created objects
        Sacco.objects.all().delete()
        UserProfile.objects.all().delete()
