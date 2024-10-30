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
from landing import views as landing_views
from subscriptions import views as subscription_views
from checkouts import views as checkout_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("old-home-page", views.old_home_page_view),
    path("", landing_views.landing_page_view, name="home"),
    path("about/", views.about_view),
    # path("my-auth/", include("myauth.urls")), # Use allauth instead
    path('accounts/', include('allauth.urls')),
    path("protected/", views.pw_protected_view),
    path("protected/user-only", views.user_only_view),
    path("protected/staff-only", views.staff_only_view),
    path("no-permission/", views.no_permission_view),
    path("profiles/", include("profiles.urls")),
    path("pricing/", subscription_views.subscription_price_view, name="pricing"),
    path("pricing/<str:interval>/", subscription_views.subscription_price_view, name="pricing_interval"),
    path("checkout/price/<int:price_id>", checkout_views.product_price_redirect_view, name="sub-price-checkout"),
    path("checkout/start/", checkout_views.cheeckout_redirect_view, name="start-stripe-checkout"),
    path("checkout/success/", checkout_views.checkout_finalize_view, name="end-stripe-checkout"),
    path("accounts/billing/", subscription_views.user_subscription_view, name="user-subscription"),
    path("accounts/billing/cancel/", subscription_views.user_subscription_cancel_view, name="user-subscription-cancel"),
    path("contact/", views.contact_view, name="contact"),
]
