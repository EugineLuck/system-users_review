from django.contrib import admin
from .models import staff, ad, system_users, applications, login_credentials,column_mapping
@admin.register(staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('pf_no', 'sam_name', 'full_name', 'email', 'supervisor', 'application')
    search_fields = ('pf_no', 'sam_name', 'email', 'full_name')
@admin.register(ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('pf_no', 'email', 'sam_name', 'system_status', 'last_login')
    search_fields = ('pf_no', 'sam_name', 'email')
@admin.register(system_users)
class SystemUsersAdmin(admin.ModelAdmin):
    list_display = ('pf_no', 'sam_name', 'full_name', 'email', 'application')
    search_fields = ('pf_no', 'sam_name', 'email')
@admin.register(applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('application_name', 'application_type', 'app_support_admin', 'department', 'number_of_users', 'data_source')
    search_fields = ('application_name', 'app_support_admin', 'department')
@admin.register(login_credentials)
class CredentialsAdmin(admin.ModelAdmin):
    list_display = ('application', 'username', 'expiry_date', 'reset_date')
    search_fields = ('application__application_name', 'username')
@admin.register(column_mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ('model_field', 'excel_header')
    search_fields = ('model_field', 'excel_header')

