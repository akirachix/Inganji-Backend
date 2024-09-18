from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import FarmersManagement

class FarmersManagementModelTest(TestCase):

    def test_create_farmers_management_with_unique_cooperative_number(self):
        farmer = FarmersManagement.objects.create(
            first_name='John',
            last_name='Njoroge',
            phone_number='07654567890',
            sacco_name='Limuru'
        )
        
        self.assertIsNotNone(farmer.cooperative_number)
        retrieved_farmer = FarmersManagement.objects.get(farmer_id=farmer.farmer_id)
        self.assertEqual(farmer.cooperative_number, retrieved_farmer.cooperative_number)
        another_farmer = FarmersManagement.objects.create(
            first_name='Jane',
            last_name='Kibaara',
            phone_number='0793462545',
            sacco_name='Kikuyu'
        )
        
        self.assertEqual(another_farmer.cooperative_number, farmer.cooperative_number + 1)

    def test_create_farmers_management_without_first_name(self):
        with self.assertRaises(ValidationError):
            farmer = FarmersManagement(
                last_name='Koigi',
                phone_number='0745-7890',
                sacco_name='Muranga'
            )
            farmer.full_clean() 

    def test_cooperative_number_cannot_be_manually_set(self):
        farmer = FarmersManagement(
            first_name='John',
            last_name='Awour',
            phone_number='07654567890',
            sacco_name='Limuru',
            cooperative_number=999 
        )
        farmer.save()
        
       