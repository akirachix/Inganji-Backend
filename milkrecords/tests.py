from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from farmers.models import FarmersManagement, Cooperative
from .models import MilkRecords
User = get_user_model()  # Ensure you are using the User model defined in your project
class MilkRecordsModelTest(TestCase):
    def setUp(self):
        # Create a user instance for the Cooperative
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        # Create a cooperative instance with a user
        self.cooperative = Cooperative.objects.create(
            cooperative_name='Test Cooperative',
            user=self.user  # Assign the created user to the cooperative
        )
        self.farmer = FarmersManagement.objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='123456789',
            created_at=timezone.now(),
            cooperative_id=self.cooperative
        )
    def test_milk_record_creation(self):
        milk_record = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=150,
            date=timezone.now()
        )
        self.assertEqual(milk_record.farmer_id, self.farmer)
        self.assertEqual(milk_record.milk_quantity, 100)
        self.assertEqual(milk_record.price, 150)
    def test_milk_record_future_date(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=150,
            date=future_date
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()
    def test_milk_record_negative_price(self):
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=-150,
            date=timezone.now()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()
    def test_milk_record_negative_quantity(self):
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=-100,
            price=150,
            date=timezone.now()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()
    def test_milk_record_str_method(self):
        milk_record = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=150,
            date=timezone.now()
        )
        self.assertEqual(str(milk_record), f"Milk record for {self.farmer} on {milk_record.date}")
    def test_milk_record_without_farmer(self):
        milk_record = MilkRecords(
            farmer_id=None,
            milk_quantity=100,
            price=150,
            date=timezone.now()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()