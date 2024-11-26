import logging
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.shortcuts import render
from .models import UnauthorizedAccessLog, BlockedIP
from django.core.mail import send_mail
from django.conf import settings


# Set up logging
logger = logging.getLogger(__name__)

# This view renders the honeypot form
def honeypot_form(request):
    return render(request, 'honeypot_form.html')

@csrf_exempt
def honeypot_view(request):
    ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")

    # Check if the IP is already blocked
    if BlockedIP.objects.filter(ip_address=ip_address).exists():
        logger.warning(f"Blocked IP attempted access: {ip_address}")
        return HttpResponseForbidden("Your IP has been blocked.")

    if request.method == "POST":
        honeypot_field = request.POST.get('honeypot_field', '')
        logger.info(f"Form Data Received: {request.POST}")

        # If the honeypot field is filled, it's likely a bot
        if honeypot_field:
            # Log unauthorized access attempt in the database
            timestamp = now()
            url_accessed = request.build_absolute_uri()
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            
            # Save the log entry to the database
            UnauthorizedAccessLog.objects.create(
                ip_address=ip_address,
                timestamp=timestamp,
                url_accessed=url_accessed,
                user_agent=user_agent
            )

            # Block the IP by adding it to the BlockedIP model
            BlockedIP.objects.create(ip_address=ip_address)

            
            

            # Respond with a forbidden message
            return JsonResponse(
                {'message': 'Access forbidden, unauthorized attempt logged and IP blocked.'}, status=403
            )

        # If honeypot_field is empty, assume legitimate form submission
        return JsonResponse({'message': 'Login successful!'}, status=200)

    # If the request method is not POST
    return JsonResponse({'message': 'Invalid request method.'}, status=400)


from .models import UnauthorizedAccessLog

def illegal_logs_view(request):
    logs = UnauthorizedAccessLog.objects.all().order_by('-timestamp') 
    context = {'logs': logs}
    return render(request, 'illegal_logs.html', context)

import matplotlib.pyplot as plt
import io
import urllib, base64
import pandas as pd
from django.shortcuts import render
from .models import UnauthorizedAccessLog

def illegal_logs_view(request):
    # Query UnauthorizedAccessLog data
    logs = UnauthorizedAccessLog.objects.all()
    
    # Create a DataFrame from the logs data
    df = pd.DataFrame(list(logs.values('user_agent')))
    
    # Count the occurrences of each user agent
    user_agent_counts = df['user_agent'].value_counts()
    
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(user_agent_counts, labels=user_agent_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image as base64
    img_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return render(request, 'illegal_logs.html', {'logs': logs, 'img_url': img_url})
