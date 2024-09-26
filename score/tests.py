from django.test import TestCase
from django.utils import timezone
from django.forms import ValidationError
from django.contrib.auth import get_user_model  # Import the user model
from farmers.models import FarmersManagement, Cooperative  # Import your Cooperative model
from .models import Score

User = get_user_model()  # Get the user model

class ScoreModelTests(TestCase):

    def setUp(self):
        # Create a User instance for the ForeignKey relationship if needed
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

        # Create a Cooperative instance for the ForeignKey relationship
        self.cooperative = Cooperative.objects.create(
            cooperative_name="Test Cooperative",
            user=self.user  # Assign the user instance here if necessary
        )

        # Create a FarmersManagement instance for the foreign key relationship
        self.farmer = FarmersManagement.objects.create(
            first_name="Alice",
            last_name="Johnson",
            phone_number="1234567890",
            created_at=timezone.now(),
            cooperative_number="12345",
            sacco_name="Co-op Dairy",
            cooperative_id=self.cooperative  # Assign the cooperative instance here
        )

    def test_valid_score(self):
        score = Score(
            farmer_id=self.farmer,
            score=700,
            credit_worthiness="Good",
            loan_range="1000-5000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        try:
            score.clean()  # This should not raise a ValidationError
        except ValidationError:
            self.fail("Score.clean() raised ValidationError unexpectedly!")

    def test_score_below_minimum(self):
        score = Score(
            farmer_id=self.farmer,
            score=-1,
            credit_worthiness="Bad",
            loan_range="0-1000",
            last_checked_date=timezone.now().date(),
            is_eligible=False
        )
        with self.assertRaises(ValidationError) as context:
            score.clean()
        self.assertEqual(str(context.exception), "['Score must be between 0 and 850.']")

    def test_score_above_maximum(self):
        score = Score(
            farmer_id=self.farmer,
            score=851,
            credit_worthiness="Excellent",
            loan_range="5000-10000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        with self.assertRaises(ValidationError) as context:
            score.clean()
        self.assertEqual(str(context.exception), "['Score must be between 0 and 850.']")

    def test_last_checked_date_in_future(self):
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        score = Score(
            farmer_id=self.farmer,
            score=700,
            credit_worthiness="Fair",
            loan_range="2000-4000",
            last_checked_date=future_date,
            is_eligible=True
        )
        with self.assertRaises(ValidationError) as context:
            score.clean()
        self.assertEqual(str(context.exception), "['Last checked date cannot be in the future.']")

    def test_string_representation(self):
        score = Score(
            farmer_id=self.farmer,
            score=700,
            credit_worthiness="Fair",
            loan_range="2000-4000",
            last_checked_date=timezone.now().date(),
            is_eligible=True
        )
        self.assertEqual(str(score), f"Score for {self.farmer}: {score.credit_score_id}")
