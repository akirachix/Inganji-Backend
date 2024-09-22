from django.test import TestCase
from farmers.models import FarmersManagement
from score.models import Score
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date

class ScoreModelTest(TestCase):

    def setUp(self):
        # Create a test farmer instance
        self.farmer = FarmersManagement.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            sacco_name="Sacco A"
        )

    def test_create_score_with_valid_data(self):
        """
        Happy path: Create a score with valid data and verify all fields.
        """
        score = Score.objects.create(
            farmer_id=self.farmer,
            score=750,
            credit_worthiness="Good",
            loan_range="$5000 - $10000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        
        # Check field values
        self.assertEqual(score.farmer_id, self.farmer)
        self.assertEqual(score.score, 750)
        self.assertEqual(score.credit_worthiness, "Good")
        self.assertEqual(score.loan_range, "$5000 - $10000")
        self.assertIsInstance(score.last_checked_date, date)
        self.assertTrue(score.is_eligible)
        self.assertEqual(str(score), f"Score for {self.farmer}: {score.credit_score_id}")

    def test_create_score_with_invalid_score(self):
        """
        Unhappy path: Test that creating a score with an invalid score raises ValidationError.
        """
        score = Score(
            farmer_id=self.farmer,
            score=900,  # Invalid score
            credit_worthiness="Good",
            loan_range="$5000 - $10000",
            last_checked_date=timezone.now().date(),
        )
        with self.assertRaises(ValidationError):
            score.full_clean()

    def test_create_score_with_empty_credit_worthiness(self):
        """
        Unhappy path: Test that creating a score with an empty credit_worthiness raises ValidationError.
        """
        score = Score(
            farmer_id=self.farmer,
            score=700,
            credit_worthiness="",  # Empty credit worthiness
            loan_range="$5000 - $10000",
            last_checked_date=timezone.now().date(),
        )
        with self.assertRaises(ValidationError):
            score.full_clean()

    def test_create_score_with_future_last_checked_date(self):
        """
        Unhappy path: Test that creating a score with a future last_checked_date raises ValidationError.
        """
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        score = Score(
            farmer_id=self.farmer,
            score=700,
            credit_worthiness="Good",
            loan_range="$5000 - $10000",
            last_checked_date=future_date,  # Future date
        )
        with self.assertRaises(ValidationError):
            score.full_clean()
