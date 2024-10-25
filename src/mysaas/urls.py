"""
URL configuration for mysaas project.

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
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("old-home-page", views.old_home_page_view),
    path("", views.home_view, name="home"),
    path("about/", views.about_view),
    # path("my-auth/", include("myauth.urls")), # Use allauth instead
    path('accounts/', include('allauth.urls')),
    path("protected/", views.pw_protected_view),
    path("protected/user-only", views.user_only_view),
    path("protected/staff-only", views.staff_only_view),
    path("no-permission/", views.no_permission_view),
    path("profiles/", include("profiles.urls")),
]
