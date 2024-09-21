from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from django.db.models import Sum
from .sms_utils import send_sms, validate_phone_number
# from .models import farmer, milk
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# from .sms_service import send_sms
import requests
from django.conf import settings
import logging



import requests
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
            f"Dear {na}, "
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





def check_eligibility():
    # farmer_id = request.POST.get('farmer_id')
    # try:
    #     farmer = Farmer.objects.get(id=farmer_id)
    # except Farmer.DoesNotExist:
    #     return JsonResponse({'error': 'Farmer not found.'}, status=404)

    is_eligible = True

    if is_eligible:
  
        message = (f"Dear jfgduhfuddd, "
                   f"Congratulations! You are eligible for a loan. "
                   f"The maximum amount you can borrow is {43333333} KSH.")
    else:
        message = (f"Dear JWYYEVWW, "
                   "We regret to inform you that you are not currently eligible for a loan. "
                  )

    headers = {
        "Authorization": f"Basic {settings.SMS_LEOPARD_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "source": "AkiraChix",
        "message": message,
        "destination": ["+254111365595"],
    }

    try:
        response = requests.post(
            settings.SMS_LEOPARD_API_URL, json=payload, headers=headers
        )
        if response.status_code != 200:
            logger.error(
                f"Failed to send message: {response.status_code} - {response.text}"
            )
            return JsonResponse({'error': 'SMS sending failed.'}, status=500)
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        return JsonResponse({'error': 'Request exception occurred.'}, status=500)


    return JsonResponse(response_data)







        

