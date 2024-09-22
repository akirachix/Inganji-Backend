from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from django.db.models import Sum
from .sms_utils import send_sms, validate_phone_number
from farmers.models import FarmersManagement
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
import logging
from rest_framework.decorators import api_view
import requests
from score.models import *
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)
def send_monthly_milk_record_sms():
    logger.info("Starting milk record SMS job")
    last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime('%B %Y')
    farmers = Farmer.objects.all()
  
        
    for farmer in farmers:
        milk_record = MilkRecord.objects.filter(farmer=farmer, date__month=datetime.now().month - 1).aggregate(total_milk=Sum('liters'))
        total_milk = milk_record['total_milk'] or 0
        total_price = self.calculate_total_price(total_milk)


        logger.info("Finished milk record SMS job")
        message = (
            f"Dear {farmer.name}, "
            f"your total milk production for {month} was {total_milk} liters, "
            f"earning you a total of {total_price} KSH."
        )
        headers = {
            "Authorization": f"Basic {settings.SMS_LEOPARD_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "source": "AkiraChix",
            "message": message,
            "destination": [{"number": phone_number}],
        }
        try:
            response = requests.post(
                settings.SMS_LEOPARD_API_URL, json=payload, headers=headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"Failed to send message: {response.status_code} - {response.text}"
                )
                return None
        except requests.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
            return None




logger = logging.getLogger(__name__)

@api_view(['POST'])
def check_eligibility(request):
    farmer_id = request.data.get('farmer_id')    
    try:
        farmer = FarmersManagement.objects.get(farmer_id=farmer_id)
        score_record = Score.objects.filter(farmer_id=farmer_id).order_by('-last_checked_date').first()

        
        if score_record:
            is_eligible = score_record.is_eligible
            loan_range = score_record.loan_range

            if is_eligible:
                message = (f"Dear {farmer.first_name} {farmer.last_name}, "
                        f"Congratulations! You are eligible for a loan. "
                        f"The amount you can borrow is between {loan_range} KSH.")

        else:
            message = (f"Dear {farmer.first_name} {farmer.last_name},"
                    "We regret to inform you that you are not currently eligible for a loan.")
            is_eligible = False

        phone_number = farmer.phone_number 
        headers = {
            "Authorization": f"Basic {settings.SMS_LEOPARD_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "source": "AkiraChix",
            "message": message,
            "destination": [{"number": phone_number}],
        }

        logger.info(f"Sending SMS with payload: {payload}")

        try:
            response = requests.post(
                settings.SMS_LEOPARD_API_URL, json=payload, headers=headers
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info("Message sent successfully!")
                else:
                    logger.error(f"Failed to send message: {result.get('message')}")
            else:
                logger.error(
                    f"Failed to send message: {response.status_code} - {response.text}"
                )
        except requests.RequestException as e:
            logger.error(f"Request exception occurred: {e}")

        return JsonResponse({'farmer_id': farmer_id, 'is_eligible': is_eligible})

    except FarmersManagement.DoesNotExist:
        return JsonResponse({'error': 'Farmer does not exist.'}, status=404)


