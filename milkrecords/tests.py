from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from farmers.models import FarmersManagement, Cooperative, Sacco
from users.models import UserProfile
from .models import MilkRecords

class MilkRecordsModelTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.cooperative = Cooperative.objects.create(
            cooperative_name='Test Cooperative',
            user=self.user
        )
        self.sacco_user = UserProfile.objects.create_user(
            username='saccouser',
            password='saccopassword',
            email='saccouser@example.com'
        )
        self.sacco = Sacco.objects.create(
            sacco_name='Test Sacco',
            user=self.sacco_user
        )
        self.farmer = FarmersManagement.objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='123456789',
            created_at=timezone.now(),
            cooperative_id=self.cooperative,
            sacco_id=self.sacco
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
        future_date = timezone.now() + timedelta(days=1)
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

    def test_zero_quantity(self):
        milk_record = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=0,
            price=150,
            date=timezone.now()
        )
        self.assertEqual(milk_record.milk_quantity, 0)

    def test_today_date(self):
        today_date = timezone.now().date()
        milk_record = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=150,
            date=today_date
        )
        self.assertEqual(milk_record.date, today_date)

    def test_multiple_records_for_same_farmer(self):
        milk_record1 = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=100,
            price=150,
            date=timezone.now()
        )
        milk_record2 = MilkRecords.objects.create(
            farmer_id=self.farmer,
            milk_quantity=200,
            price=300,
            date=timezone.now()
        )
        self.assertNotEqual(milk_record1.pk, milk_record2.pk)

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

    def test_milk_record_without_quantity_and_price(self):
        milk_record = MilkRecords(
            farmer_id=self.farmer,
            milk_quantity=None,
            price=None,
            date=timezone.now()
        )
        with self.assertRaises(ValidationError):
            milk_record.full_clean()
