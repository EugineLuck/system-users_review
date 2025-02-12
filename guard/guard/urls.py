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
from access_review import views
admin.site.site_header='USERS ACCESS REVIEW ADMIN DASHBOARD'
admin.site.site_title='Users Review'
admin.site.index_title='DATA CENTRE'
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('sandbox/', views.sandbox, name='sandbox'),
    path('employees/', views.employees, name='employees'),
    path('insights/', views.insights, name='insights'),
    path('finacle/', views.finacle, name='finacle'),
    path('active_directory/', views.active_directory, name='active_directory'),
    path("upload_excel/", views.upload_excel, name='upload_excel'),
    path('save_mappings/', views.save_mappings, name='save_mappings'),
    path('savejdbc/', views.savejdbc, name='savejdbc'),
    path('get_model_fields/', views.get_model_fields, name='get_model_fields'),
    path('jdbc_connections/', views.jdbc_connections, name='jdbc_connections'),
    path('filter-users/', views.filter_users, name='filter_users'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
