from django.urls import path
from .views import  check_eligibility

urlpatterns = [
    path('', check_eligibility, name='check_eligibility'),
]
