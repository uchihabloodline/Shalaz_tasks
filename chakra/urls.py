"""chakra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from API import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('signup', views.user_signup, name = "signup user"),
	path('login', views.user_login, name = "login user"),
	path('logout', views.user_logout, name = "login user"),
	path('post_create', views.post_create, name = "login user"),
	path('post_list', views.post_list_all, name = "login user"),
	path('fetch_restaurents/<search>/<location_name>/<int:page_number>/<int:count>', views.fetch_restaurents, name = "fetch restaurents"),
	path('favourite', views.favourite_get, name="favourite restaurent"),
	path('favourite/<int:res_id>', views.favourite, name="favourite get restaurent"),
	path('schedule/<int:res_id>/<int:schedule_time>/<int:guests>', views.schedule, name="schedule restaurent")
]