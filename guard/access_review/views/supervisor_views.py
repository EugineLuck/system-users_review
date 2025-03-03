from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import staff, line_manager,applications
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
@csrf_exempt
def supervisor_query(request):
    if request.method == 'POST':
        try:
            # Fetch All Unique Supervisors
            supervisors = staff.objects.values_list('supervisor_pf', flat=True).distinct()
            supervisors_list = list(supervisors)  # Convert QuerySet to list

            print(f"Total Supervisors Found: {len(supervisors_list)}")
            print(f"First 5 entries: {supervisors_list[:5]}")  # First 5
            print(f"Last 5 entries: {supervisors_list[-5:]}")  # Last 5 (Now Supported 🔥🔥)

            updated_count = 0

            for supervisor in supervisors_list:
                if supervisor:  # Skip Empty Supervisors
                    supervisor_data = staff.objects.filter(pf_no=str(supervisor)).values(
                        'pf_no', 'sam_name', 'email', 'full_name', 'employee_status',
                        'subsidiary', 'department', 'title', 'branch', 'actual_end_date'
                    ).first()

                    if supervisor_data:
                        line_manager.objects.update_or_create(
                            pf_no=supervisor_data['pf_no'],
                            defaults=supervisor_data
                        )
                        updated_count += 1

            return JsonResponse({'message': f'{updated_count} Supervisors updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'access_review/supervisor.html')
def supervisor_t(request):
    try:
        applications_list = list(applications.objects.values_list('application_name', flat=True))
        sys_count = len(applications_list)

        subsidiaries = list(line_manager.objects.order_by('subsidiary').values_list('subsidiary', flat=True).distinct())

   
        users = list(line_manager.objects.all().values())

        user_count = len(users)

        paginator = Paginator(users, 20000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'access_review/supervisor.html', {
            'applications': applications_list,
            'managers': page_obj,
            'user_count': user_count,
            'sys_count': sys_count,
            'page_obj': page_obj,
            'subsidiaries': subsidiaries
        })

    except ObjectDoesNotExist as e:
        print(f"An error occurred: {e}")
        return render(request, 'access_review/supervisor.html', {
            'applications': None,
            'managers': None,
            'user_count': 0,
            'sys_count': 0
        })
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return render(request, 'access_review/supervisor.html', {
            'applications': None,
            'managers': None,
            'user_count': 0
        })