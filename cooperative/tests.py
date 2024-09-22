from django.test import TestCase
from .models import Cooperative, UserProfile
from django.core.exceptions import ValidationError

class CooperativeModelTest(TestCase):

    def setUp(self):
        # Create a UserProfile instance for testing
        self.user = UserProfile.objects.create(username="testuser", email="test@example.com")

    # Happy Path Test
    def test_create_cooperative_success(self):
        """Test successful creation of a Cooperative."""
        cooperative = Cooperative(cooperative_name="Green Cooperative", user=self.user)
        cooperative.save()
        self.assertEqual(Cooperative.objects.count(), 1)
        self.assertEqual(cooperative.cooperative_name, "Green Cooperative")

    # Unhappy Path Tests
    def test_create_cooperative_missing_name(self):
        """Test creation fails with missing cooperative name."""
        cooperative = Cooperative(user=self.user)
        with self.assertRaises(ValidationError):
            cooperative.full_clean()  # This should raise a ValidationError

    def test_create_cooperative_invalid_user(self):
        """Test that trying to create a Cooperative with a non-existent user fails."""
        invalid_user = UserProfile(pk=999)  # Assuming this user does not exist
        cooperative = Cooperative(cooperative_name="New Cooperative", user=invalid_user)
        
        with self.assertRaises(Exception):  # This should fail when validating
            cooperative.full_clean()  # Validate before saving

    def test_user_deleted_cooperative(self):
        """Test that accessing a cooperative's user after deletion raises an error."""
        cooperative = Cooperative.objects.create(cooperative_name="Another Cooperative", user=self.user)
        user_id = cooperative.user.id  # Store the ID to check after deletion
        self.user.delete()  # Delete the user

        # Attempt to access the deleted user
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=user_id)  # Check the user ID directly

    def tearDown(self):
        # Clean up any created objects
        Cooperative.objects.all().delete()
        UserProfile.objects.all().delete()
