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
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from bhp_personnel.admin_site import bhp_personnel_admin

from .admin_site import timesheet_admin
from .views import HomeView

app_name = 'timesheet'

urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('timesheet_dashboard/', include('timesheet_dashboard.urls')),

    path('personnel-admin/', bhp_personnel_admin.urls),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),

    path('administrator/', timesheet_admin.urls),
    path('home/', HomeView.as_view(), name='timesheet_home_url'),
    path('', HomeView.as_view(), name='timesheet_home_url'),
]
