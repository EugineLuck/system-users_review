from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMessage
from ..models import staff, system_users
import pandas as pd
import os

# Function to send email
def send_email(subject, body, recipient_list, cc_list=None, attachment_path=None):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
        cc=cc_list,
    )
    if attachment_path:
        with open(attachment_path, 'rb') as file:
            email.attach_file(attachment_path)
    email.send()

# Main logic
def share_supervisor_data(request):
    try:
        # Fetch Staff data
        staff_data = staff.objects.filter(employee_status='Active').values(
            'pf_no', 'full_name', 'email', 'supervisor_pf'
        )
        staff_df = pd.DataFrame(staff_data)

        # Fetch System Users data
        system_users_data = system_users.objects.all().values(
            'application', 'pf_no', 'user_id', 'sam_name', 'email', 'system_status',
            'creation_date', 'last_login', 'system_role', 'subsidiary'
        )
        system_users_df = pd.DataFrame(system_users_data)

        # Get Supervisor details
        supervisors_df = staff_df[['pf_no', 'full_name', 'email', 'supervisor_pf']].copy()
        supervisors_df = supervisors_df.merge(
            staff_df[['pf_no', 'email']],
            left_on='supervisor_pf',
            right_on='pf_no',
            suffixes=('', '_supervisor')
        )
        supervisors_df = supervisors_df.rename(columns={'email_supervisor': 'supervisor_email'})
        supervisors_df = supervisors_df[['full_name', 'email', 'pf_no', 'supervisor_email']].drop_duplicates()

        # Merge System Users with Staff
        systems_df = system_users_df.merge(staff_df, left_on='sam_name', right_on='sam_name')
        systems_df = systems_df[[
            'application', 'pf_no', 'user_id', 'sam_name', 'email', 'system_status',
            'creation_date', 'last_login', 'system_role', 'subsidiary', 'supervisor_pf'
        ]]

        # Filter System and Staff data for each supervisor
        for _, supervisor in supervisors_df.iterrows():
            supervisor_pf = supervisor['pf_no']
            supervisor_email = supervisor['supervisor_email']

            # Filter System Data
            system_data = systems_df[systems_df['supervisor_pf'] == supervisor_pf]
            system_data_file = f"system_data_{supervisor_pf}.csv"
            system_data.to_csv(system_data_file, index=False)

            # Filter Staff Data
            staff_data = staff_df[staff_df['supervisor_pf'] == supervisor_pf]
            staff_data_file = f"staff_data_{supervisor_pf}.csv"
            staff_data.to_csv(staff_data_file, index=False)

            # Send email to supervisor
            subject = f"System and Staff Data for Supervisor {supervisor['full_name']}"
            body = f"""
            Dear {supervisor['full_name']},
           
            I trust this message finds you well.

            Please find attached the system and staff data report for your team as part of the Users Recertification Test Exercise.

            Kindly review the information for your reference.

            Kind regards,
            Eugine Wanyama
            IT Governance Department
            Equity Bank


            """
            recipient_list = [supervisor_email, 'Eugine.wanyama@equitybank.co.ke']  # Default email included
            send_email(subject, body, recipient_list, attachment_path=system_data_file)

            # Log email status
            print(f"Email shared to {supervisor_email} with data for PF {supervisor_pf}.")

            # Clean up files
            os.remove(system_data_file)
            os.remove(staff_data_file)

        # Render success message on the front end
        return render(request, 'line_manager_review.html', {'message': 'Emails shared successfully with supervisors.'})

    except Exception as e:
        # Render error message on the front end
        return render(request, 'line_manager_review.html', {'error_message': str(e)})