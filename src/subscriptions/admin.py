from django.contrib import admin

# Register your models here.
from . models import Subscription, UserSubscription
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(Subscription)
admin.site.register(UserSubscription)