from django.contrib import admin
from .models import staff, ad, system_users, applications, login_credentials,column_mapping,definition_of_headers,role_matrix,line_manager
@admin.register(staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('pf_no', 'sam_name', 'full_name', 'email', 'supervisor', 'application')
    search_fields = ('pf_no', 'sam_name', 'email', 'full_name')
@admin.register(line_manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('pf_no', 'sam_name', 'full_name', 'email', 'branch')
    search_fields = ('pf_no', 'sam_name', 'email', 'full_name','branch')
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
    list_display = ('application_name', 'application_type', 'app_support_admin_email','tier','department', 'number_of_users', 'data_source')
    search_fields = ('application_name', 'app_support_admin_email','tier' 'department')
@admin.register(login_credentials)
class CredentialsAdmin(admin.ModelAdmin):
    list_display = ('application', 'username', 'expiry_date', 'reset_date')
    search_fields = ('application__application_name', 'username')
@admin.register(column_mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ('model_field', 'excel_header')
    search_fields = ('model_field', 'excel_header')

@admin.register(definition_of_headers)
class HeadersAdmin(admin.ModelAdmin):
    list_display = ('header', 'description','example')
    search_fields = ('header', 'description','example')

@admin.register(role_matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ('application','role_id', 'role_name','owners')
    search_fields = ('application','role_id', 'role_name','owners')
