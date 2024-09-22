
import random
from datetime import datetime, timedelta
import logging
from django.conf import settings
from .sms_utils import send_sms, validate_phone_number
from .models import farmer, milk
from django.db.models import Sum

logger = logging.getLogger(__name__)

def send_milk_record_sms():
    last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime('%B %Y')

    farmers = Farmer.objects.all()

    for farmer in farmers:
        milk_record = MilkRecord.objects.filter(farmer=farmer, date__month=datetime.now().month - 1).aggregate(total_milk=Sum('liters'))
        
        total_milk = milk_record['total_milk'] or 0
        total_price = calculate_total_price(total_milk) 

        message = format_sms_message(farmer.name, last_month, total_milk, total_price)
        phone = farmer.phone 

        print(f"Message to be sent: {message}")

        send_sms_to_farmer(farmer.name, message, phone)

    logger.info("Finished milk record SMS job")

def format_sms_message(farmer, month, total_milk, total_price):
    return (
        f"Dear {farmer}, "
        f"your total milk production for {month} was {total_milk} liters, "
        f"earning you a total of {total_price} KSH."
    )

def calculate_total_price(total_milk):
    return total_milk * price_per_liter

def send_sms_to_farmer(farmer, message, phone):
    print(f"Sending SMS to {farmer}: {message} at {phone}")
    response = send_sms(phone, message)
    print(f"SMS response: {response}")
    if response and response.get('success'):
        logger.info(f"SMS sent successfully to {farmer} at {phone}.")
    else:
        logger.error(f"Failed to send SMS to {farmer} at {phone}: {response}")






import random
import logging
from django.conf import settings
from .sms_utils import send_sms
from .models import farmer

logger = logging.getLogger(__name__)

def send_loan_eligibility_sms(farmer):
    min_loan_amount = farmer.min_loan_amount
    max_loan_amount = farmer.max_loan_amount
    phone = farmer.phone  
    farmer_name = farmer.name
    message = format_loan_eligibility_message(farmer_name, min_loan_amount, max_loan_amount)
    
    logger.info(f"Sending loan eligibility SMS to {farmer_name} at {phone}: {message}")
    
    result = send_sms_to_farmer(farmer_name, message, phone)
    
    logger.info("Finished loan eligibility SMS job")
    return result

def format_loan_eligibility_message(farmer, min_amount, max_amount):
    return (
        f"Dear {farmer}, "
        f"you are eligible for a loan. "
        f"You can borrow between {min_amount} and {max_amount} KSH."
    )

def send_sms_to_farmer(farmer, message, phone):
    logger.info(f"Sending SMS: {message} to {phone}")
    response = send_sms(phone, message)
    if response and response.get('success'):
        logger.info(f"Loan eligibility SMS sent successfully to {farmer} at {phone}.")
        return True
    else:
        logger.error(f"Failed to send loan eligibility SMS to {farmer} at {phone}: {response}")
        return False

def process_loan_eligibility():
    farmers = Farmer.objects.all()  

    for farmer in farmers:
        is_eligible, min_loan_amount, max_loan_amount = check_loan_eligibility(farmer)
        
        if is_eligible:
            message = format_loan_eligibility_message(farmer.name, min_loan_amount, max_loan_amount)
            send_sms_to_farmer(farmer.name, message, farmer.phone)
        else:
            logger.info(f"Farmer {farmer.name} is not eligible for a loan at this time.")

if __name__ == "__main__":
    process_loan_eligibility()







        
