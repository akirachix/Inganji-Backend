from django.test import TestCase
from farmers.models import FarmersManagement
from django.utils import timezone
from django.core.exceptions import ValidationError

class FarmersManagementModelTest(TestCase):

    def test_create_farmer_with_valid_data(self):
        """
        Happy path: Create a farmer with valid data and verify that all fields are correct.
        Ensure the cooperative number is generated correctly.
        """
        farmer = FarmersManagement.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            sacco_name="Sacco A"
        )
        # Check field values
        self.assertEqual(farmer.first_name, "John")
        self.assertEqual(farmer.last_name, "Doe")
        self.assertEqual(farmer.phone_number, "1234567890")
        self.assertEqual(farmer.sacco_name, "Sacco A")
        
        # Ensure cooperative number is generated
        self.assertIsNotNone(farmer.cooperative_number)
        self.assertTrue(farmer.cooperative_number.startswith(f"C/{timezone.now().year}/"))
        
        # Check the string representation
        self.assertEqual(farmer.__str__(), "John Doe")


class FarmersManagementInvalidModelTest(TestCase):
    
    def test_create_farmer_with_too_long_first_name(self):
        """
        Unhappy path: Test that creating a farmer with a first name exceeding max_length raises ValidationError.
        """
        farmer = FarmersManagement(
            first_name="A" * 51,  # exceeds max_length of 50
            last_name="Doe",
            phone_number="1234567890",
            sacco_name="Sacco A"
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
            sacco_name="Sacco A"
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
            last_name="Doe",
            phone_number="InvalidPhone",  # Non-numeric phone number
            sacco_name="Sacco A"
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
            last_name="Doe",
            phone_number="1234567890",
            sacco_name="S" * 21  # exceeds max_length of 20
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
            last_name="Doe",
            phone_number="1234567890",
            sacco_name="Sacco A",
            cooperative_number="C/2024/1"  # Manually set cooperative number
        )
        
        # Second farmer with duplicate cooperative number
        farmer2 = FarmersManagement(
            first_name="Jane",
            last_name="Smith",
            phone_number="0987654321",
            sacco_name="Sacco B",
            cooperative_number="C/2024/1"  # Duplicate cooperative number
        )
        # Validate and expect a ValidationError
        with self.assertRaises(ValidationError):
            farmer2.full_clean()
