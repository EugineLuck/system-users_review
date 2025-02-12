from django.shortcuts import render
import pandas as pd
from ldap3 import Server, Connection, ALL, SUBTREE
from datetime import datetime
from .models import login_credentials, ad, applications, column_mapping, system_users, staff
from django.http import JsonResponse
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.db.models import Count
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.cache import cache

def index(request):
    return render(request, 'access_review/index.html')

def jdbc_connections(request):
    try:
        applications_list = list(applications.objects.values('id', 'application_name'))

        return render(request, 'access_review/jdbc_connections.html', {
            'applications': applications_list,
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, 'access_review/jdbc_connections.html', {
            'applications': [],
        })

def fetch_ad_user_data(username):
    AD_SERVER = 'ldap://ebsafrica.com'
    AD_BASE_DN = 'DC=ebsafrica,DC=com'
    try:
        application = applications.objects.get(application_name='AD')
        cred = login_credentials.objects.filter(application=application).first()
        if not cred:
            return "No AD login_credentials found."
        ad_username = cred.username  
        password = cred.password 
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=ad_username, password=password, authentication='SIMPLE')
        if not conn.bind():
            return f"Failed to connect: {conn.result}"
        search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
        attributes = ['sAMAccountName', 'cn', 'mail', 'physicalDeliveryOfficeName', 'department', 
                      'description', 'userAccountControl', 'accountExpires', 'pwdLastSet', 'lastLogon']
        conn.search(search_base=AD_BASE_DN, search_filter=search_filter, attributes=attributes, search_scope=SUBTREE)
        if not conn.entries:
            return f"User {username} not found in AD."
        user = conn.entries[0]
        return {
            "sam_name": user.sAMAccountName.value if 'sAMAccountName' in user else None,
            "full_name": user.cn.value if 'cn' in user else None,
            "email": user.mail.value if 'mail' in user else None
        }
    except Exception as e:
        return f"An error occurred: {str(e)}"

def fetch_ad_data():
    AD_SERVER = 'ldap://ebsafrica.com'
    AD_BASE_DN = 'DC=ebsafrica,DC=com'
    try:
        application = applications.objects.get(application_name='AD')
        cred = login_credentials.objects.filter(application=application).first()
        if not cred:
            return "No AD login_credentials found."
        username = cred.username  
        password = cred.password 
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=username, password=password, authentication='SIMPLE')
        if not conn.bind():
            return f"Failed to connect: {conn.result}"
        user_data = []
        search_filter = '(&(objectClass=user)(objectCategory=person))'
        attributes = ['sAMAccountName', 'cn', 'mail', 'physicalDeliveryOfficeName', 'department', 
                      'description', 'userAccountControl', 'accountExpires', 'pwdLastSet', 'lastLogon']
        conn.search(search_base=AD_BASE_DN, search_filter=search_filter, attributes=attributes, search_scope=SUBTREE)
        for entry in conn.entries:
            user = entry
            def convert_timestamp(attr):
                if attr is None:
                    return None
                try:
                    return datetime.fromtimestamp(int(attr) / 10000000 - 11644473600)
                except (ValueError, TypeError):
                    return None
            pwd_last_set = convert_timestamp(user.pwdLastSet.value if 'pwdLastSet' in user else None)
            last_logon = convert_timestamp(user.lastLogon.value if 'lastLogon' in user else None)
            account_active = "Yes" if int(user.userAccountControl.value) & 2 == 0 else "No"
            user_data.append({
                "pf_no": user.physicalDeliveryOfficeName.value if 'physicalDeliveryOfficeName' in user else None,
                "sam_name": user.sAMAccountName.value if 'sAMAccountName' in user else None,
                "full_name": user.cn.value if 'cn' in user else None,
                "email": user.mail.value if 'mail' in user else None,
                "department": user.department.value if 'department' in user else None,
                "description": user.description.value if 'description' in user else None,
                "account_active": account_active,
                "account_expires": convert_timestamp(user.accountExpires.value if 'accountExpires' in user else None),
                "pwd_last_set": pwd_last_set,
                "last_logon": last_logon,
            })
        df = pd.DataFrame(user_data)
        for _, row in df.iterrows():
            email = row['email'] if row['email'] else 'no-email@domain.com'
            ad.objects.update_or_create(
                pf_no=row['pf_no'],
                defaults={
                    'sam_name': row['sam_name'],
                    'full_name': row['full_name'],
                    'email': email,  
                    'system_status': row['account_active'],
                    'last_login': row['last_logon'],
                    'password_last_set': row['pwd_last_set'],
                    'password_expired': row.get('password_expired'),
                    'creation_date': row.get('creation_date'),
                    'account_expiration_date': row.get('account_expiration_date'),
                    'system_role': row.get('system_role'),
                    'organization_unit': row.get('organization_unit'),
                    'when_changed': row.get('when_changed'),
                    'subsidiary': row.get('subsidiary'),
                    'application': 'AD'
                }
            )
    except Exception as e:
        return f"An error occurred: {str(e)}"

def home(request):
    try:
        applications_list = None
        users = None
        user_count = 0
        sys_count = 0
        subsidiaries = None
        applications_list = cache.get('applications_list')
        if not applications_list:
            applications_list = list(applications.objects.values_list('application_name', flat=True))
            cache.set('applications_list', applications_list, timeout=6 * 1)
            sys_count = len(applications_list)
        subsidiaries = cache.get('subsidiaries')
        if not subsidiaries:
            subsidiaries = list(
                staff.objects.order_by('subsidiary').values_list('subsidiary', flat=True).distinct()
            )
            cache.set('subsidiaries', subsidiaries, timeout=6 * 5)
        users = cache.get('system_users')
        if not users:
            users = list(system_users.objects.values_list(
                'application','pf_no',  'user_id','sam_name', 'email', 'system_status', 'creation_date','last_login', 'system_role','subsidiary'
            ))
            cache.set('system_users', users, timeout=60 * 15)
        user_count = len(users)
        paginator = Paginator(users, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'access_review/home.html', {
            'applications': applications_list,
            'users': page_obj,
            'user_count': user_count,
            'sys_count': sys_count,
            'page_obj': page_obj,
            'subsidiaries': subsidiaries
        })
    except ObjectDoesNotExist as e:
        print(f"An error occurred: {e}")
        return render(request, 'access_review/home.html', {
            'applications': None,
            'users': None,
            'user_count': 0,
            'sys_count': 0
        })
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return render(request, 'access_review/home.html', {
            'applications': None,
            'users': None,
            'user_count': 0
        })

def employees(request):
    try:
        applications_list = None
        users = None
        user_count = 0
        sys_count = 0
        subsidiaries = None
        applications_list = list(applications.objects.values_list('application_name', flat=True))
        sys_count = len(applications_list)
        subsidiaries = list(
            staff.objects.order_by('subsidiary').values_list('subsidiary', flat=True).distinct()
        )
        category = request.GET.get("category", "active")
        print(f"📌 Category requested: {category}")

        category_filter = {
            "active": ["Active Assignment"],
            "suspended": ["Suspend Assignment", "Suspend Paid Assignment"],
            "ex_employees": ["Ex Employee"],
            "contingent": ["Contingent"],
            "service_accounts": ["Service Account"],
        }.get(category, ["Active Assignment"])  # Default to Active Assignment

        # Fetch users directly (no cache)
        users = list(staff.objects.filter(employee_status__in=category_filter).values(
            "pf_no", "full_name", "email", "supervisor", "supervisor_pf", "employee_category", 
            "department", "subsidiary", "title", "branch", "actual_end_date"
        ))

        user_count = len(users)
        print(f"✅ Users fetched: {user_count}")

        # Pagination
        paginator = Paginator(users, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'access_review/employees.html', {
            'applications': applications_list,
            'users': page_obj,
            'user_count': user_count,
            'sys_count': sys_count,
            'page_obj': page_obj,
            'subsidiaries': subsidiaries
        })

    except ObjectDoesNotExist as e:
        print(f"❌ ObjectDoesNotExist Error: {e}")
        return render(request, 'access_review/employees.html', {
            'applications': None,
            'users': None,
            'user_count': 0,
            'sys_count': 0
        })
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return render(request, 'access_review/employees.html', {
            'applications': None,
            'users': None,
            'user_count': 0
        })


def login_to_ad(username, password):
    AD_SERVER = 'ldap://ebsafrica.com'
    DOMAIN = 'ebsafrica.com'
    user_dn = f'{username}@{DOMAIN}'
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=user_dn, password=password, authentication='SIMPLE')
    if conn.bind():
        return "Login successful"
    else:
        return f"Login failed: {conn.last_error}"

@csrf_exempt
def upload_excel(request):
    print("POST request received")
    if request.method == "POST" and request.FILES.get("file"):
        print("File upload detected")
        try:
            uploaded_file = request.FILES["file"]
            print(f"Received file: {uploaded_file.name}")
            print(f"File size: {uploaded_file.size} bytes")
            df = pd.read_excel(uploaded_file, sheet_name=0)
            excel_headers = df.columns.tolist()
            excel_name = os.path.splitext(uploaded_file.name)[0]
            print(f"Excel headers: {excel_headers}")
            return JsonResponse({"excel_headers": excel_headers, "excel_name": excel_name})
        except Exception as e:
            print(f"Error processing file: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    return render(request, "access_review/upload_excel.html")

def get_model_fields(request):
    model_name = request.GET.get("model_name")
    if not model_name:
       return JsonResponse({"error": "No model selected."}, status=400)
    try:
        model = apps.get_model("access_review", model_name)
        all_fields = [field.name for field in model._meta.fields]
        model_fields_mapping = {
            "ad": [
                'pf_no', 'sam_name', 'full_name', 'email', 'system_status', 'last_login',
                'password_last_set', 'password_expired', 'creation_date',
                'account_expiration_date', 'system_role', 'organization_unit',
                'when_changed', 'subsidiary', 'application'
            ],
            "system_users": [
                'pf_no', 'sam_name', 'user_id', 'full_name', 'email', 'creation_date',
                'system_status', 'last_login', 'branch', 'system_role', 'work_class',
                'role_id', 'subsidiary', 'application'
            ],
            "staff": [
                'pf_no', 'sam_name', 'full_name', 'email', 'supervisor', 'supervisor_pf',
                'employee_category', 'employee_status', 'subsidiary', 'department',
                'title', 'branch', 'actual_end_date', 'application'
            ]
        }
        model_fields = [field for field in all_fields if field in model_fields_mapping.get(model_name, [])]
        return JsonResponse({"model_fields": model_fields, "model_name": model_name}, safe=False)
    except LookupError:
        return JsonResponse({"error": "Model not found."}, status=404)

@csrf_exempt
def save_mappings(request):
    if request.method == "POST":
        try:
            print(f"we are here to save files ")
            data = json.loads(request.body)
            application = data.get('model_name')  
            mappings = data.get('mappings', [])
            if not application or not mappings:
                return JsonResponse({"error": "Application or mappings missing"}, status=400)
            for mapping in mappings:
                column_mapping.objects.create(
                    model_field=mapping['model_field'],
                    excel_header=mapping['excel_header'],
                    application=application
                )
            print(f"saved successfully ")
            return JsonResponse({"message": "Mappings saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def savejdbc(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            application_id = data.get('application')
            username = data.get('username')
            password = data.get('password')
            host = data.get('host')
            port = data.get('port')
            service_name = data.get('service_name')
            login_credentials.objects.create(
                username=username,
                password=password,
                application_id=application_id,
                host=host,
                port=port,
                service_name=service_name
            )
            return JsonResponse({"message": "JDBC connection saved successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def filter_users(request):
    audit_filter = request.GET.get('audit_filter')
    application_id = request.GET.get('application_id')
    users = ad.objects.all()
    if application_id:
        users = users.filter(application_id=application_id)
    if audit_filter:
        if audit_filter == "Access Violations":
            users = users.filter(system_status="Violation")
        elif audit_filter == "Duplicate Accounts":
            duplicate_sam_names = (
                ad.objects.values('sam_name')
                .annotate(count=Count('id'))
                .filter(count__gt=1)
                .values_list('sam_name', flat=True)
            )
            users = users.filter(sam_name__in=duplicate_sam_names)
        elif audit_filter == "Idle Users":
            users = users.filter(last_login__lt=timezone.now() - timezone.timedelta(days=90))
        elif audit_filter == "Dormant Accounts":
            users = users.filter(system_status="Dormant")
        elif audit_filter == "Data Mismatch":
            users = users.filter(email__isnull=True)
    user_count = users.count()
    users_data = [
        {
            "pf_no": user.pf_no,
            "sam_name": user.sam_name,
            "user_id": user.organization_unit,
            "email": user.email,
            "system_status": user.system_status,
            "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "",
            "application": user.application if user.application else "",
        }
        for user in users
    ]
    return JsonResponse({
        "users": users_data,
        "user_count": user_count,
    })
    