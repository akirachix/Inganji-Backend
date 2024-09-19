from django.test import TestCase

from django.test import TestCase
from django.utils import timezone
from farmer.models import Farmer
from score.models import Score

class ScoreModelTest(TestCase):
    def setUp(self):
        self.farmer = Farmer.objects.create(
            name="Test Farmer"
        )
        
        self.score = Score.objects.create(
            farmer=self.farmer,
            score=85,
            credit_worthiness="medium",
            loan_range="1000-5000",
            last_checked_date=timezone.now().date(),
            status="eligible"
        )

    def test_default_farmer(self):
       self.assertEqual(self.score.farmer.farmer_id, self.farmer.farmer_id)

  
