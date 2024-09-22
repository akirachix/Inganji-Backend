from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import FarmersManagement

class FarmersManagementModelTest(TestCase):

    def test_create_farmer_invalid_first_name(self):
        """Test creation fails with an invalid first name (e.g., too short)."""
        farmer = FarmersManagement(first_name="J", last_name="Doe", phone_number="1234567890", sacco_name="Test Sacco")
        with self.assertRaises(ValidationError):
            farmer.full_clean()  # This should raise a ValidationError

    def test_create_farmer_invalid_phone_number(self):
        """Test creation fails with an invalid phone number (e.g., non-numeric)."""
        farmer = FarmersManagement(first_name="John", last_name="Doe", phone_number="abc", sacco_name="Test Sacco")
        with self.assertRaises(ValidationError):
            farmer.full_clean()  # This should raise a ValidationError

    def test_create_farmer_success(self):
        """Test successful creation of a farmer."""
        farmer = FarmersManagement(first_name="John", last_name="Doe", phone_number="1234567890", sacco_name="Test Sacco")
        farmer.full_clean()  # Validate the instance
        farmer.save()
        self.assertEqual(FarmersManagement.objects.count(), 1)
        self.assertEqual(farmer.first_name, "John")

    def test_create_farmer_with_duplicate_phone_number(self):
        """Test creation fails with a duplicate phone number."""
        FarmersManagement.objects.create(first_name="Jane", last_name="Doe", phone_number="1234567890", sacco_name="Test Sacco")
        farmer = FarmersManagement(first_name="John", last_name="Smith", phone_number="1234567890", sacco_name="Test Sacco")
        with self.assertRaises(ValidationError):
            farmer.full_clean()  # This should raise a ValidationError

    def test_create_farmer_with_missing_fields(self):
        """Test creation fails with missing required fields."""
        farmer = FarmersManagement(last_name="Doe", phone_number="1234567890", sacco_name="Test Sacco")  # Missing first name
        with self.assertRaises(ValidationError):
            farmer.full_clean()  # This should raise a ValidationError
