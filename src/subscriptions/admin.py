from django.contrib import admin

# Register your models here.
from . models import Subscription, UserSubscription, SubscriptionPrice
from django.contrib.auth.models import Permission

class SubscriptionPriceAdmin(admin.TabularInline):
    model = SubscriptionPrice
    readonly_fields = ["stripe_id"]
    can_delete = False
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPriceAdmin]
    list_display = ["name", "active"]
    readonly_fields = ["stripe_id"]

admin.site.register(Permission)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)