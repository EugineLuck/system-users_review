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
    app_support_admin = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)
    number_of_users = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'applications'
        verbose_name_plural = 'applications'

    def __str__(self):
        return f"App Name: {self.application_name}, Admin: {self.app_support_admin}, Source: {self.data_source}"
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
