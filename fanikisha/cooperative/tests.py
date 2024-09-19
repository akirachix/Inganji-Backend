from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Cooperative

class CooperativeModelTest(TestCase):
    def setUp(self):
        self.cooperative_data = {
            'cooperative_name': 'Test Cooperative'
        }
    def test_create_cooperative_success(self):
        cooperative = Cooperative.objects.create(**self.cooperative_data)
        self.assertEqual(Cooperative.objects.count(), 1)
        self.assertEqual(cooperative.cooperative_name, self.cooperative_data['cooperative_name'])

    def test_cooperative_str_method(self):
        cooperative = Cooperative.objects.create(**self.cooperative_data)
        self.assertEqual(str(cooperative), self.cooperative_data['cooperative_name'])

    def test_cooperative_name_max_length(self):
        long_name = 'x' * 256  
        cooperative = Cooperative(cooperative_name=long_name)
        with self.assertRaises(ValidationError):
            cooperative.full_clean()

    def test_cooperative_name_blank(self):
        cooperative = Cooperative(cooperative_name='')
        with self.assertRaises(ValidationError):
            cooperative.full_clean()

    def test_duplicate_cooperative_name(self):
        Cooperative.objects.create(**self.cooperative_data)
        duplicate_cooperative = Cooperative.objects.create(**self.cooperative_data)
        self.assertEqual(Cooperative.objects.count(), 2)
        self.assertNotEqual(duplicate_cooperative.cooperative_id, 1)

    def test_cooperative_id_auto_increment(self):
        first_cooperative = Cooperative.objects.create(**self.cooperative_data)
        second_cooperative = Cooperative.objects.create(cooperative_name='Another Cooperative')
        self.assertEqual(second_cooperative.cooperative_id, first_cooperative.cooperative_id + 1)