from django.db import models

class staff(models.Model):
    pf_no = models.CharField(max_length=50, null=True, blank=True)
    sam_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    supervisor = models.CharField(max_length=200, null=True, blank=True)
    supervisor_pf = models.CharField(max_length=50, null=True, blank=True)
    employee_category = models.CharField(max_length=100, null=True, blank=True)
    employee_status = models.CharField(max_length=100, null=True, blank=True)
    subsidiary = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    actual_end_date = models.CharField(max_length=100, null=True, blank=True)
    application = models.CharField(max_length=200, null=True, blank=True)
    supervisor_email = models.EmailField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'staff'
        verbose_name = 'staff'
        verbose_name_plural = 'staff'

    def __str__(self):
        return f"PF No: {self.pf_no}, Email: {self.email}, SAM Name: {self.sam_name}"


class line_manager(models.Model):
    pf_no = models.CharField(max_length=50, null=True, blank=True)
    sam_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    employee_status = models.CharField(max_length=100, null=True, blank=True)
    subsidiary = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    actual_end_date = models.CharField(max_length=100, null=True, blank=True)
  

    class Meta:
        db_table = 'line_manager'
        verbose_name = 'line_manager'
        verbose_name_plural = 'line_manager'

    def __str__(self):
        return f"PF No: {self.pf_no}, Email: {self.email}, SAM Name: {self.sam_name}, Location : {self.branch}"

class ad(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    sam_name = models.CharField(max_length=100, null=True, blank=True)
    system_status = models.CharField(max_length=50, null=True, blank=True)
    pf_no = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    password_last_set = models.CharField(max_length=200, null=True, blank=True)
    password_never_expires = models.CharField(max_length=200, null=True, blank=True)
    password_expired = models.CharField(max_length=200, null=True, blank=True)
    last_login = models.CharField(max_length=200, null=True, blank=True)
    creation_date = models.CharField(max_length=200, null=True, blank=True)
    account_expiration_date = models.CharField(max_length=200, null=True, blank=True)
    system_role = models.CharField(max_length=100, null=True, blank=True)
    organization_unit = models.CharField(max_length=200, null=True, blank=True)
    when_changed = models.CharField(max_length=200, null=True, blank=True)
    subsidiary = models.CharField(max_length=100, null=True, blank=True)
    application = models.CharField(max_length=200, null=True, blank=True)
    system_violations = models.CharField(max_length=10, null=True, blank=True)
    unidentified = models.CharField(max_length=100, null=True, blank=True)
    dormancy = models.CharField(max_length=100, null=True, blank=True)
    aging = models.CharField(max_length=50, null=True, blank=True)
    duplicates = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    exception = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'ad'
        verbose_name = 'ad'
        verbose_name_plural = 'ad'

    def __str__(self):
        return f"PF No: {self.pf_no}, Email: {self.email}, SAM Name: {self.sam_name}"

class system_users(models.Model):
    pf_no = models.CharField(max_length=50, null=True, blank=True)
    sam_name = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    creation_date = models.CharField(max_length=200, null=True, blank=True)
    system_status = models.CharField(max_length=50, null=True, blank=True)
    last_login = models.CharField(max_length=200, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    system_role = models.CharField(max_length=100, null=True, blank=True)
    work_class = models.CharField(max_length=100, null=True, blank=True)
    role_id = models.CharField(max_length=100, null=True, blank=True)
    subsidiary = models.CharField(max_length=100, null=True, blank=True)
    application = models.CharField(max_length=200, null=True, blank=True)
    system_violations = models.CharField(max_length=10, null=True, blank=True)
    unidentified = models.CharField(max_length=100, null=True, blank=True)
    dormancy = models.CharField(max_length=100, null=True, blank=True)
    aging = models.CharField(max_length=50, null=True, blank=True)
    duplicates = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    organization_unit = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'system_users'
        verbose_name = 'system_users'
        verbose_name_plural = 'system_users'

    def __str__(self):
        return f"PF No: {self.pf_no}, Email: {self.email}, SAM Name: {self.sam_name}, App Name: {self.application}"

class applications(models.Model):
    APPLICATION_TYPES = [
        ('on_premise', 'On Premise'),
        ('third_party', 'Third Party'),
        ('user_portal', 'User Portal'),
    ]
    data_source = models.CharField(max_length=200, null=True, blank=True)
    application_name = models.CharField(max_length=200, null=True, blank=True)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPES, null=True, blank=True)
    app_description = models.TextField(null=True, blank=True)
    app_support_admin_email = models.CharField(max_length=200, null=True, blank=True)
    tier =models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)
    number_of_users = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'applications'
        verbose_name_plural = 'applications'

    def __str__(self):
        return f"App Name: {self.application_name}, Admin: {self.app_support_admin_email}, Source: {self.data_source}"
class login_credentials(models.Model):
    application = models.ForeignKey(applications, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    reset_date = models.DateTimeField(null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    port = models.CharField(max_length=200, null=True, blank=True)
    service_name = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'login_credentials'
        verbose_name = 'login_credentials'
        verbose_name_plural = 'login_credentials'

    def __str__(self):
        return f"App Name: {self.application.application_name if self.application else 'N/A'}, Username: {self.username}, Expiry Date: {self.expiry_date}"
class column_mapping(models.Model):
    model_field = models.CharField(max_length=255)
    excel_header = models.CharField(max_length=255)
    application = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'column_mapping'
        verbose_name = 'column_mapping'
        verbose_name_plural = 'column_mapping'

    def __str__(self):
        return f"{self.model_field} -> {self.excel_header}"
class definition_of_headers(models.Model):
    header = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    example = models.TextField( null=True, blank=True)
   

    class Meta:
        db_table = 'definition_of_headers'
        verbose_name = 'definition_of_headers'
        verbose_name_plural = 'definition_of_headers'

    def __str__(self):
        return f"header: {self.header}, description: {self.description},  example: {self.example}"
    
class role_matrix(models.Model):
    role_id = models.TextField(null=True, blank=True)
    application = models.CharField(max_length=255, null=True, blank=True)
    role_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owners = models.TextField(null=True, blank=True)
    access_level = models.TextField(null=True, blank=True)
    modules = models.TextField(null=True, blank=True)
    menu = models.TextField(null=True, blank=True)
    transaction_type = models.TextField(null=True, blank=True)
    sod = models.TextField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    account_expiration_date = models.TextField(null=True, blank=True)
    permissions = models.TextField(null=True, blank=True)
    frequency = models.TextField(null=True, blank=True)
    approval = models.TextField(null=True, blank=True)
    hr_terms = models.TextField(null=True, blank=True)
    reporting_structure = models.TextField(null=True, blank=True)
    audit_trail = models.TextField(null=True, blank=True)
    time_based = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "role_matrix"
        verbose_name = "Role Matrix"
        verbose_name_plural = "Role Matrices"

    def __str__(self):
        return f"Application Name: {self.application}, Role ID: {self.role_id}, Role Name: {self.role_name}, Owners: {self.owners}"
