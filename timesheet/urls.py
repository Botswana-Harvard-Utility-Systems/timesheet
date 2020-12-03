"""timesheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic.base import RedirectView
from bhp_personnel.admin_site import bhp_personnel_admin

from .admin_site import timesheet_admin
from .views import HomeView, AdministrationView

app_name = 'timesheet'

urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),
    
    path('admin/', admin.site.urls),
    path('admin/', timesheet_admin.urls),
    path('admin/', bhp_personnel_admin.urls),
    
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('admin/', RedirectView.as_view(url='admin/timesheet/'),
         name='timesheet_models_url'),
    

    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('subject/', include('timesheet_dashboard.urls')),
    
    
    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]
