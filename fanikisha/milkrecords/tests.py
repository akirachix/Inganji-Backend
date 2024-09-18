from django.test import TestCase
from django.utils import timezone
from farmers.models import FarmersManagement
from .models import MilkRecords
from django.core.exceptions import ValidationError

class MilkRecordsModelTest(TestCase):

    def setUp(self):
        self.farmer = FarmersManagement.objects.create(
            first_name='John',
            last_name='Njoroge',
            phone_number='0756567890',
            sacco_name='Test Co-op'
        )

    def test_milk_record_creation(self):
        """Happy path: Milk record is created successfully."""
        milk_record = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=10,
            price=50,
            date=timezone.now().date()
        )
        self.assertIsInstance(milk_record, MilkRecords)
        self.assertEqual(milk_record.milk_quantity, 10)
        self.assertEqual(milk_record.price, 50)

    def test_milk_record_negative_quantity(self):
        """Unhappy path: Milk quantity cannot be negative."""
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=-5,
            price=50,
            date=timezone.now().date()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()

    def test_milk_record_negative_price(self):
        """Unhappy path: Price cannot be negative."""
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=10,
            price=-50,
            date=timezone.now().date()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()

    def test_milk_record_future_date(self):
        """Unhappy path: Date cannot be in the future."""
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=10,
            price=50,
            date=future_date
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()

    def test_milk_record_str_method(self):
        """Happy path: Ensure the __str__ method returns the expected string."""
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=10,
            price=50,
            date=timezone.now().date()
        )
        expected_str = f"Milk record for {self.farmer} on {milk_record.date}"
        self.assertEqual(str(milk_record), expected_str)

    def test_milk_record_without_farmer(self):
        """Unhappy path: MilkRecords cannot be created without a farmer."""
        milk_record = MilkRecords(
            farmer_id=None,  # This should raise an error
            milk_quantity=10,
            price=50,
            date=timezone.now().date()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()