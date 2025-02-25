from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from fuzzywuzzy import process
import pandas as pd
from ..models import role_matrix, definition_of_headers, staff, system_users

def count_distinct_roles():
    roles_list = role_matrix.objects.values_list('role_id', flat=True).order_by('role_id').distinct()
    all_roles = [role.split(',') for role in roles_list if role]
    distinct_roles = {role.strip() for sublist in all_roles for role in sublist}
    return len(distinct_roles)

def role_matrix_view(request):
    try:
        category = request.GET.get("category", "headers") 

        print(f"📌 Category requested: {category}")

        # Fetch data based on the category
        if category == "headers":
            data = list(definition_of_headers.objects.values('header', 'description', 'example'))
            paginator = Paginator(data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'headers': page_obj,  
                'page_obj': page_obj,
            }

        elif category == "roles":
            data = list(role_matrix.objects.values.all())
            paginator = Paginator(data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'roles': page_obj,
                'page_obj': page_obj,
            }
            # Print first 5 roles for debugging
            print(f"📋 Roles data (first 5): {data[:5]}")
        
        elif category == "user_mappings":
            mappings = process_user_mapping()
            context = {
                'user_mapping': mappings,
            }
            # Print first 5 user mappings for debugging
            print(f"📋 User mappings data (first 5): {mappings.head().to_dict('records') if not mappings.empty else 'No data'}")
        
        elif category == "maker_checker":
            maker_checker = check_maker_checker()
            context = {
                'maker_checker': maker_checker,
            }
            # Print maker_checker result for debugging
            print(f"📋 Maker Checker result: {maker_checker}")
        
        elif category == "sys_limits":
            syst_lim = 'to be validated by the business'
            context = {
                'limits': syst_lim,
            }
            # Print system limits for debugging
            print(f"📋 System Limits: {syst_lim}")
        
        else:
            # Default to headers
            data = list(definition_of_headers.objects.values_list('header', flat=True))
            paginator = Paginator(data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'headers': page_obj,
                'page_obj': page_obj,
            }
            # Print first 5 headers for debugging
            print(f"📋 Default Headers data (first 5): {data[:5]}")

        # Common data for all categories
        applications_list = list(role_matrix.objects.values_list('application', flat=True).order_by('application').distinct())
        sys_count = len(applications_list)
        subsidiaries = list(staff.objects.order_by('subsidiary').values_list('subsidiary', flat=True).distinct())
        roles_count = count_distinct_roles()

        context.update({
            'applications': applications_list,
            'roles_count': roles_count,
            'sys_count': sys_count,
            'subsidiaries': subsidiaries,
        })

        # Print common data for debugging
        print(f"📋 Applications list (first 5): {applications_list[:5]}")
        print(f"📋 Subsidiaries list (first 5): {subsidiaries[:5]}")
        print(f"📋 Roles count: {roles_count}")

        return render(request, 'access_review/role_matrix.html', context)

    except ObjectDoesNotExist as e:
        print(f"❌ ObjectDoesNotExist Error: {e}")
        return render(request, 'access_review/role_matrix.html', {
            'applications': None,
            'headers': None,
            'limits': None,
            'maker_checker': None,
            'user_mapping': None,
            'roles': None,
            'roles_count': 0
        })
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return render(request, 'access_review/role_matrix.html', {
            'applications': None,
            'headers': None,
            'limits': None,
            'maker_checker': None,
            'user_mapping': None,
            'roles': None,
            'roles_count': 0
        })

def fuzzy_lookup(role, role_matrix):
    if not role_matrix.exists():
        return None

    role_ids = role_matrix.values_list('role_id', flat=True)
    if not role_ids:
        return None

    match, score = process.extractOne(str(role), role_ids)
    return match if score > 80 else None

def check_maker_checker():
    roles = role_matrix.objects.all()
    maker_checker_roles = ['maker', 'checker', 'inputer', 'verifier']
    for role in roles:
        if any(mcr in role.role_id.lower() for mcr in maker_checker_roles):
            return True
    return False

def process_user_mapping(application_name=None):
    users = system_users.objects.values('application', 'sam_name', 'email', 'pf_no', 'system_role')
    hr_title = staff.objects.values('sam_name', 'title', 'department')
    roles = role_matrix.objects.all()

    users_df = pd.DataFrame(list(users))
    roles_df = pd.DataFrame(list(roles))
    hr_title_df = pd.DataFrame(list(hr_title))

    if application_name:
        users_df = users_df[users_df['application'] == application_name]

    merged_df = pd.merge(users_df, hr_title_df, on='sam_name', how='inner')

    matched_roles = []
    for _, row in merged_df.iterrows():
        system_role = row['system_role']
        matched_role = fuzzy_lookup(system_role, roles)
        if matched_role:
            role_details = roles_df[roles_df['role_id'] == matched_role].iloc[0].to_dict()
            matched_roles.append({**row.to_dict(), **role_details})

    result_df = pd.DataFrame(matched_roles)
    return result_df