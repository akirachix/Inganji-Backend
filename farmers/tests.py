from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import UserProfile  # Adjust the import as per your actual user model
from farmers.models import FarmersManagement
from cooperative.models import Cooperative


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.valid_user_data = {
            "username": "ivymwaurak",
            "password": "ivy12345",
            "email": "ivy@example.com",
            "first_name": "Ivy",
            "last_name": "Wanjiku",
            "role": "sacco"
        }
        # Create the initial user for the test
        self.existing_user = UserProfile.objects.create_user(**self.valid_user_data)

    def test_create_user_with_valid_data(self):
        """
        Happy path: Create a user with valid data and verify that all fields are correct.
        """
        user = UserProfile.objects.create_user(
            username="newuser",
            password="newpassword",
            email="new@example.com",
            first_name="New",
            last_name="User",
            role="sacco"
        )
        
        # Check field values
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.role, "sacco")

def test_create_user_with_duplicate_username(self):
    """
    Unhappy path: Test that creating a user with a duplicate username raises ValidationError.
    """
    # First, create a user with a unique username
    unique_user_data = {
        "username": "peterk",
        "password": "password123",
        "email": "peterk@example.com",
        "first_name": "Peyer",
        "last_name": "Koigi",
        "role": "sacco"
    }
    
    UserProfile.objects.create_user(**unique_user_data)

    # Now try to create a second user with the same username
    duplicate_user_data = {
        "username": "peterk",  # This is the same username as above
        "password": "password1234",
        "email": "peterkk@example.com",
        "first_name": "Peteer",
        "last_name": "User",
        "role": "sacco"
    }

    with self.assertRaises(ValidationError):
        UserProfile.objects.create_user(**duplicate_user_data)


    def test_create_user_with_invalid_email(self):
        """
        Unhappy path: Test that creating a user with an invalid email raises ValidationError.
        """
        invalid_email_user_data = {
            "username": "newuser2",
            "password": "password123",
            "email": "invalidemail.com",  # Invalid email
            "first_name": "New",
            "last_name": "User",
            "role": "sacco"
        }

        with self.assertRaises(ValidationError):
            UserProfile.objects.create_user(**invalid_email_user_data)


class FarmersManagementModelTest(TestCase):

    def setUp(self):
        self.some_user_profile_instance = UserProfile.objects.create_user(
            username="exampleuser",
            password="password",
            email="example@example.com",
            first_name="Example",
            last_name="User",
            role="sacco"
        )
        self.cooperative = Cooperative.objects.create(cooperative_name="Coop Test", user=self.some_user_profile_instance)

    def test_create_farmer_with_valid_data(self):
        """
        Happy path: Create a farmer with valid data and verify that all fields are correct.
        Ensure the cooperative number is generated correctly.
        """
        farmer = FarmersManagement.objects.create(
            first_name="John",
            last_name="Kamau",
            phone_number="074567890",
            sacco_name="Sacco A",
            cooperative_id=self.cooperative
        )
        # Check field values
        self.assertEqual(farmer.first_name, "John")
        self.assertEqual(farmer.last_name, "Kamau")
        self.assertEqual(farmer.phone_number, "074567890")
        self.assertEqual(farmer.sacco_name, "Sacco A")
        
        # Ensure cooperative number is generated
        self.assertIsNotNone(farmer.cooperative_number)
        self.assertTrue(farmer.cooperative_number.startswith(f"C/{timezone.now().year}/"))
        
        # Check the string representation
        self.assertEqual(farmer.__str__(), "John Kamau")


class FarmersManagementInvalidModelTest(TestCase):

    def setUp(self):
        self.some_user_profile_instance = UserProfile.objects.create_user(
            username="exampleuser2",
            password="password",
            email="example2@example.com",
            first_name="Example",
            last_name="User",
            role="sacco"
        )
        # Create a cooperative to use in the tests
        self.cooperative = Cooperative.objects.create(cooperative_name="Coop Test", user=self.some_user_profile_instance)

    def test_create_farmer_with_too_long_first_name(self):
        """
        Unhappy path: Test that creating a farmer with a first name exceeding max_length raises ValidationError.
        """
        farmer = FarmersManagement(
            first_name="A" * 51,  # exceeds max_length of 50
            last_name="Kamau",
            phone_number="1234567890",
            sacco_name="Sacco A",
            cooperative_id=self.cooperative
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer.full_clean()  # Triggers validation

    def test_create_farmer_with_too_long_last_name(self):
        """
        Unhappy path: Test that creating a farmer with a last name exceeding max_length raises ValidationError.
        """
        farmer = FarmersManagement(
            first_name="John",
            last_name="B" * 51,  # exceeds max_length of 50
            phone_number="1234567890",
            sacco_name="Sacco A",
            cooperative_id=self.cooperative
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer.full_clean()

    def test_create_farmer_with_non_numeric_phone_number(self):
        """
        Unhappy path: Test that creating a farmer with a non-numeric phone number raises ValidationError.
        """
        farmer = FarmersManagement(
            first_name="John",
            last_name="Kamau",
            phone_number="InvalidPhone",  # Non-numeric phone number
            sacco_name="Sacco A",
            cooperative_id=self.cooperative
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer.full_clean()

    def test_create_farmer_with_too_long_sacco_name(self):
        """
        Unhappy path: Test that creating a farmer with a sacco name exceeding max_length raises ValidationError.
        """
        farmer = FarmersManagement(
            first_name="John",
            last_name="Kamau",
            phone_number="074567890",
            sacco_name="S" * 21,  # exceeds max_length of 20
            cooperative_id=self.cooperative
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer.full_clean()

    def test_create_farmer_with_duplicate_cooperative_number(self):
        """
        Unhappy path: Test that creating a farmer with a duplicate cooperative number raises ValidationError.
        """
        # First farmer
        FarmersManagement.objects.create(
            first_name="John",
            last_name="Kamu",
            phone_number="07567890",
            sacco_name="Sacco A",
            cooperative_number="C/2024/1",  # Manually set cooperative number
            cooperative_id=self.cooperative
        )
        
        # Second farmer with duplicate cooperative number
        farmer2 = FarmersManagement(
            first_name="Jane",
            last_name="Njeri",
            phone_number="0987654321",
            sacco_name="Sacco B",
            cooperative_number="C/2024/1",  # Duplicate cooperative number
            cooperative_id=self.cooperative
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer2.full_clean()
