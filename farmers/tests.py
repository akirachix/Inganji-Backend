from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import UserProfile  
from farmers.models import FarmersManagement
from cooperative.models import Cooperative
from sacco.models import Sacco  

class FarmersManagementModelTest(TestCase):

    def setUp(self):
        self.user_profile_instance = UserProfile.objects.create_user(
            username="exampleuser",
            password="password",
            email="example@example.com",
            first_name="Wangari",
            last_name="Mutiso",
            role="sacco"
        )
        self.cooperative = Cooperative.objects.create(cooperative_name="Coop Test", user=self.user_profile_instance)
        self.sacco = Sacco.objects.create(sacco_name="Sacco A", user=self.user_profile_instance)

    def test_create_farmer_with_valid_data(self):
        farmer = FarmersManagement.objects.create(
            first_name="John",
            last_name="Kimani",
            phone_number="074567890",
            sacco_id=self.sacco,
            cooperative_id=self.cooperative
        )
        self.assertEqual(farmer.first_name, "John")
        self.assertEqual(farmer.last_name, "Kimani")
        self.assertEqual(farmer.phone_number, "074567890")
        self.assertEqual(farmer.sacco_id, self.sacco)
        self.assertIsNotNone(farmer.cooperative_number)
        self.assertTrue(farmer.cooperative_number.startswith(f"C/{timezone.now().year}/"))
        self.assertEqual(farmer.__str__(), "John Kimani")

class FarmersManagementInvalidModelTest(TestCase):

    def setUp(self):
        self.user_profile_instance = UserProfile.objects.create_user(
            username="exampleuser2",
            password="password",
            email="example2@example.com",
            first_name="Karanja",
            last_name="Wambua",
            role="sacco"
        )
        self.cooperative = Cooperative.objects.create(cooperative_name="Coop Test", user=self.user_profile_instance)
        self.sacco = Sacco.objects.create(sacco_name="Sacco A", user=self.user_profile_instance)

    def test_create_farmer_with_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            farmer = FarmersManagement(
                first_name="Jane",
                last_name="Akinyi",
                phone_number="invalid_phone",
                sacco_id=self.sacco,
                cooperative_id=self.cooperative
            )
            farmer.full_clean()

    def test_create_farmer_without_first_name(self):
        with self.assertRaises(ValidationError):
            farmer = FarmersManagement(
                first_name="",
                last_name="Akinyi",
                phone_number="074567890",
                sacco_id=self.sacco,
                cooperative_id=self.cooperative
            )
            farmer.full_clean()

    def test_create_farmer_without_last_name(self):
        with self.assertRaises(ValidationError):
            farmer = FarmersManagement(
                first_name="Jane",
                last_name="",
                phone_number="074567890",
                sacco_id=self.sacco,
                cooperative_id=self.cooperative
            )
            farmer.full_clean()

    def test_create_farmer_with_invalid_cooperative(self):
        with self.assertRaises(ValidationError):
            farmer = FarmersManagement(
                first_name="John",
                last_name="Wambua",
                phone_number="074567890",
                sacco_id=self.sacco,
                cooperative_id=None
            )
            farmer.full_clean()
