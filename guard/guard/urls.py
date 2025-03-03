"""
URL configuration for guard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from access_review.views import home_views,roles_views,send_email_views,sandbox_view,supervisor_views
admin.site.site_header='USERS ACCESS REVIEW ADMIN DASHBOARD'
admin.site.site_title='Users Review'
admin.site.index_title='DATA CENTRE'
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.index, name='index'),
    path('home/', home_views.home, name='home'),
    path('sandbox/', home_views.sandbox, name='sandbox'),
    path('employees/', home_views.employees, name='employees'),
    path('insights/', home_views.insights, name='insights'),
    path('line_manager/', home_views.line_manager, name='line_manager'),
    path('finacle/', home_views.finacle, name='finacle'),
    path('role_matrix/', roles_views.role_matrix_view, name='role_matrix'),
    path('user_review/', home_views.user_review, name='user_review'),
    path('active_directory/', home_views.active_directory, name='active_directory'),
    path("upload_excel/", home_views.upload_excel, name='upload_excel'),
    path('save_mappings/', home_views.save_mappings, name='save_mappings'),
    path('savejdbc/', home_views.savejdbc, name='savejdbc'),
    path('get_model_fields/', home_views.get_model_fields, name='get_model_fields'),
    path('jdbc_connections/', home_views.jdbc_connections, name='jdbc_connections'),
    path('filter-users/', home_views.filter_users, name='filter_users'),
    path('send_email/', send_email_views.send_email, name='send_email'),
    path('share_supervisor_data/', sandbox_view.share_supervisor_data, name='share_supervisor_data'),
    path('update_supervisor/', supervisor_views.supervisor_query, name='update_supervisor'),
    path('supervisor_t/', supervisor_views.supervisor_t, name='supervisor_t'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
