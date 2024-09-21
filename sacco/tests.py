from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Sacco

class SaccoModelTest(TestCase):
    def setUp(self):
        self.sacco_data = {
            'sacco_name': 'Test Sacco'
        }

    def test_create_sacco_success(self):
        sacco = Sacco.objects.create(**self.sacco_data)
        self.assertEqual(Sacco.objects.count(), 1)
        self.assertEqual(sacco.sacco_name, self.sacco_data['sacco_name'])

    def test_sacco_str_method(self):
        sacco = Sacco.objects.create(**self.sacco_data)
        self.assertEqual(str(sacco), self.sacco_data['sacco_name'])

    def test_sacco_name_max_length(self):
        long_name = 'x' * 256   
        sacco = Sacco(sacco_name=long_name)
        with self.assertRaises(ValidationError):
            sacco.full_clean()

    def test_sacco_name_blank(self):
        sacco = Sacco(sacco_name='')
        with self.assertRaises(ValidationError):
            sacco.full_clean()

    def test_duplicate_sacco_name(self):
        Sacco.objects.create(**self.sacco_data)
        duplicate_sacco = Sacco.objects.create(**self.sacco_data)
        self.assertEqual(Sacco.objects.count(), 2)
        self.assertNotEqual(duplicate_sacco.sacco_id, 1)

    def test_sacco_id_auto_increment(self):
        first_sacco = Sacco.objects.create(**self.sacco_data)
        second_sacco = Sacco.objects.create(sacco_name='Another Sacco')
        self.assertEqual(second_sacco.sacco_id, first_sacco.sacco_id + 1)

  
    def test_sacco_name_type_conversion(self):
        sacco = Sacco(sacco_name=123)
        sacco.full_clean()
        self.assertEqual(sacco.sacco_name, "123")
        self.assertIsInstance(sacco.sacco_name, str)

    def test_sacco_id_read_only(self):
        sacco = Sacco.objects.create(**self.sacco_data)
        original_id = sacco.sacco_id
        
        sacco.sacco_id = 999
        sacco.save()
        
        sacco.refresh_from_db()
        
        sacco.sacco_id = 999
        sacco.save()
        
        sacco.refresh_from_db()
