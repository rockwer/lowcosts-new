"""new_lowcosts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from general.views import home, landing, search_history, get_all_requests, get_search_results
from ac_wizzair.views import flight_search_form, get_wizzair_airports

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('landing/', landing, name='landing'),
    path('search/', flight_search_form, name='search'),
    path('history/', search_history, name='history'),
    path('requests/', get_all_requests, name='all-requests'),
    re_path('results/(?P<request_id>[\w{}.-]{1,12})/', get_search_results, name='search-results'),
    re_path('update/(?P<city_code>[\w{}.-]{1,3})/', get_wizzair_airports, name='update-iata'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
