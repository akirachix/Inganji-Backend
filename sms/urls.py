from django.urls import path
from .cron import send_milk_record_sms, send_loan_eligibility_sms

urlpatterns = [
    path('send_loan-eligibility/', send_loan_eligibility_sms, name='send_loan_eligibility_sms'),
    path('send_milk_record_sms/', send_milk_record_sms, name='send_milk_record_sms'),
]
