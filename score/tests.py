from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from farmers.models import FarmersManagement
from sacco.models import Sacco
from cooperative.models import Cooperative
from users.models import UserProfile
from datetime import timedelta
from .models import Score

class ScoreModelTest(TestCase):

    def setUp(self):
     
        self.user = UserProfile.objects.create(username="testuser")
        self.cooperative = Cooperative.objects.create(cooperative_name="Test Cooperative", user=self.user)
        self.sacco = Sacco.objects.create(sacco_name="Test Sacco", user=self.user)
        self.farmer = FarmersManagement.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            sacco_id=self.sacco,
            cooperative_id=self.cooperative
        )

    def test_valid_score(self):
        # Create a valid score instance
        score = Score.objects.create(
            farmer_id=self.farmer,
            score=750,
            credit_worthiness="Good",
            loan_range="1000-5000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        # Ensure no validation error is raised
        try:
            score.clean()
        except ValidationError:
            self.fail("Valid score raised ValidationError")

    def test_invalid_score_too_high(self):
        # Test for score greater than 850
        score = Score(
            farmer_id=self.farmer,
            score=900,
            credit_worthiness="Excellent",
            loan_range="10000-15000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        with self.assertRaises(ValidationError) as cm:
            score.clean()
        self.assertIn("Score must be between 0 and 850", str(cm.exception))

    def test_invalid_score_too_low(self):
        # Test for score less than 0
        score = Score(
            farmer_id=self.farmer,
            score=-10,
            credit_worthiness="Poor",
            loan_range="0-1000",
            last_checked_date=timezone.now().date(),
            is_eligible=False
        )
        with self.assertRaises(ValidationError) as cm:
            score.clean()
        self.assertIn("Score must be between 0 and 850", str(cm.exception))

    def test_last_checked_date_in_future(self):
        # Test for last checked date in the future
        future_date = timezone.now().date() + timedelta(days=1)
        score = Score(
            farmer_id=self.farmer,
            score=600,
            credit_worthiness="Fair",
            loan_range="5000-10000",
            last_checked_date=future_date,
            is_eligible=False
        )
        with self.assertRaises(ValidationError) as cm:
            score.clean()
        self.assertIn("Last checked date cannot be in the future", str(cm.exception))

    def test_last_checked_date_today(self):
        # Test for last checked date set to today
        today = timezone.now().date()
        score = Score.objects.create(
            farmer_id=self.farmer,
            score=650,
            credit_worthiness="Good",
            loan_range="1000-5000",
            last_checked_date=today,
            is_eligible=True
        )
        try:
            score.clean()
        except ValidationError:
            self.fail("Valid score with today's date raised ValidationError")
