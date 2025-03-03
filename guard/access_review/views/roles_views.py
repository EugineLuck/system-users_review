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
            data = list(role_matrix.objects.values())
            paginator = Paginator(data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'roles': page_obj,
                'page_obj': page_obj,
                
            }
                
        elif category == "roles_mapping":
            mappings = process_user_mapping()

            context = {
                'roles_mapping': mappings.to_dict('records'), 
            }

                
        
        elif category == "maker_checker":
            maker_checker = check_maker_checker()

            # Convert DataFrame to a list of dictionaries
            maker_checker_data = maker_checker.to_dict('records') if not maker_checker.empty else []

            # Print the data for debugging
            print(f"📋 Maker Checker data: {maker_checker_data}")

            # Prepare context for the template
            context = {
                'maker_checker': maker_checker_data,
                'category': category,
            }

        
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



def check_maker_checker():
    """
    Check for maker/checker or inputer/verifier roles in the role matrix and system users.
    Returns a DataFrame with distinct applications and their status.
    """
    # Fetch data from models
    roles = role_matrix.objects.all().values('role_id', 'role_name', 'application')
    roles_df = pd.DataFrame(list(roles))

    # Keywords to search for
    keywords = ["maker", "checker", "inputer", "verifier"]

    # Fuzzy search to find roles containing the keywords
    maker_checker_apps = set()
    for _, row in roles_df.iterrows():
        role_id = str(row['role_id'])
        role_name = str(row['role_name'])
        
        # Check if role_id or role_name contains any of the keywords
        for keyword in keywords:
            if process.extractOne(keyword, [role_id, role_name], score_cutoff=80):
                maker_checker_apps.add(row['application'])
                break

    # Create a DataFrame to store applications with maker/checker or inputer/verifier
    maker_checker_df = pd.DataFrame({
        'application': list(maker_checker_apps),
        'status': 'maker checker or inputer verifier found'
    })

    if maker_checker_df.empty:
        print("No applications with maker/checker or inputer/verifier roles found.")
        return pd.DataFrame()

    # Fetch system users for the identified applications
    applications_list = maker_checker_df['application'].tolist()
    users = system_users.objects.filter(application__in=applications_list).values('sam_name', 'system_role', 'application')
    users_df = pd.DataFrame(list(users))

    if users_df.empty:
        print("No users found for the identified applications.")
        return maker_checker_df

    # Check for maker/checker violations
    violations = []
    for app in applications_list:
        app_users_df = users_df[users_df['application'] == app]
        role_counts = app_users_df.groupby('sam_name')['system_role'].apply(list).reset_index()

        has_violation = False
        for _, row in role_counts.iterrows():
            roles = row['system_role']

            # Check if the user has both maker and checker or inputer and verifier roles
            has_maker = any("maker" in role.lower() or "inputer" in role.lower() for role in roles)
            has_checker = any("checker" in role.lower() or "verifier" in role.lower() for role in roles)

            if has_maker and has_checker:
                has_violation = True
                break

        # Set the status based on whether there are violations
        status = "maker checker To be validated" if has_violation else "maker checker effective"
        violations.append({
            'application': app,
            'status': status
        })

    # Create a DataFrame for violations
    violations_df = pd.DataFrame(violations)

    # Merge with the original maker_checker_df
    final_df = pd.merge(maker_checker_df, violations_df, on='application', how='left')
    final_df['status'] = final_df['status_y'].fillna(final_df['status_x'])

    # Drop unnecessary columns and duplicates
    final_df = final_df[['application', 'status']].drop_duplicates()

    return final_df
def fuzzy_lookup(role, role_matrix):
    if not role_matrix.exists():
        return None

    role_ids = role_matrix.values_list('role_id', flat=True)
    if not role_ids:
        return None

    match, score = process.extractOne(str(role), role_ids)
    return match if score > 80 else None



def process_user_mapping(application_name=None):
    # Fetch data from models
    applications_list = list(role_matrix.objects.values_list('application', flat=True).order_by('application').distinct())
    applications_list = [app for app in applications_list if app]  

    # Fetch active users for the specified applications
    users = system_users.objects.values('application', 'sam_name', 'email', 'pf_no', 'system_role').filter(
        system_status='Active',
        application__in=applications_list
    )

    # Fetch HR titles and roles
    hr_title = staff.objects.values('sam_name', 'title', 'department')
    roles = role_matrix.objects.values()

    # Convert QuerySets to DataFrames
    users_df = pd.DataFrame(list(users))
    hr_title_df = pd.DataFrame(list(hr_title))
    roles_df = pd.DataFrame(list(roles))

    # Check if DataFrames are not empty
    if users_df.empty or hr_title_df.empty or roles_df.empty:
        print("⚠️ One of the DataFrames is empty!")
        return pd.DataFrame()

    # Optional filter by application name
    if application_name:
        users_df = users_df[users_df['application'] == application_name]

    # Merge Users with HR Title
    merged_df = pd.merge(users_df, hr_title_df, on='sam_name', how='inner')

    # Ensure the application in the merged DataFrame matches the role matrix application
    matched_roles = []
    for _, row in merged_df.iterrows():
        system_role = row['system_role']
        application = row['application']

        # Filter roles DataFrame by application
        roles_filtered = roles_df[roles_df['application'] == application]

        # Perform fuzzy lookup for the role
        matched_role = fuzzy_lookup(system_role, role_matrix.objects.filter(application=application))

        if matched_role:
            # Convert role_id to string before filtering
            role_details = roles_filtered[roles_filtered['role_id'].astype(str) == str(matched_role)]

            if not role_details.empty:
                # Combine user data with role details
                matched_roles.append({**row.to_dict(), **role_details.iloc[0].to_dict()})

    # Return the final DataFrame
    result_df = pd.DataFrame(matched_roles)
    return result_df if not result_df.empty else pd.DataFrame()

