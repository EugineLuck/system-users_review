from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from ..models import staff
import pandas as pd
import os

def send_email(subject, body, recipient_list, file_path):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )

    # Attach file if path exists
    if file_path and os.path.exists(file_path):
        email.attach_file(file_path)

    email.send()

@csrf_exempt
def share_supervisor_data(request):
    if request.method == 'POST':
        try:
            # Fetch active staff data
            staff_data = staff.objects.filter(employee_status='Active Assignment').values('pf_no', 'full_name', 'email', 'department')
            staff_df = pd.DataFrame(staff_data)

            if staff_df.empty:
                return JsonResponse({'status': 'error', 'message': 'No active staff data found.'})

            print("Few rows of staff_df:")
            print(staff_df.head())

            # Save the data into Excel
            file_path = 'sandbox_users.xlsx'
            staff_df.to_excel(file_path, index=False)

            subject = "User Access Review Notification"
            body = """
            Dear David & George,

            Please find the attached list of active staff for user access review.

            Power BI Dashboard Link:
            https://app.powerbi.com/links/4Tmh1ejKc2?ctid=2d65fea0-8478-44f2-ac0f-1a58b1382aa2&pbi_source=linkShare&bookmarkGuid=788057f5-864a-41aa-8ba3-620f040ecad5

            Thank you.
            """
            recipient_list = ['david.ngungu1@equitybank.co.ke', 'george.kimemia@equitybank.co.ke']

            # Send email with attachment
            send_email(subject, body, recipient_list, file_path)

            return JsonResponse({'status': 'success', 'message': 'Emails sent successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

