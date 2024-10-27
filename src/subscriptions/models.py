from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.urls import reverse

import helpers.billing

User = settings.AUTH_USER_MODEL

SUBSCRIPTION_PERMISSIONS = [
    ("basic", "Basic Permission"),
    ("pro", "Pro Permission"),
    ("adbanced", "Advanced Permission"),
    ("basic_ai", "Basic AI Permission"),
]

ALLOW_CUSTOM_GROUPS = True

# Create your models here.
class Subscription(models.Model):
    """
    Subscription Plan = Stripe Product
    """
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS],
    })
    stripe_id = models.CharField(max_length=30, null=True, blank=True)
    order = models.IntegerField(default=-1, help_text=''
                    'Ordering on Django pricing page')
    featured = models.BooleanField(default=True, help_text=''
                    'Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text=" "
                    "Benefits of a plan, separated by new line", 
                    blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)

    def get_features_as_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split("\n")]

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.stripe_id or not self.stripe_id.startswith('prod_'):
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={
                    "subscription_plan_id": self.id,
                }
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order", "featured", "-updated"]
        permissions = SUBSCRIPTION_PERMISSIONS


class SubscriptionPrice(models.Model):
    """
    Subscription Price = Stripe Price
    """
    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    stripe_id = models.CharField(max_length=50, null=True, blank=True)
    interval = models.CharField(max_length=30, 
                                default=IntervalChoices.MONTHLY,
                                choices=IntervalChoices.choices
                            )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text=''
                    'Ordering on Django pricing page')
    featured = models.BooleanField(default=True, help_text=''
                    'Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["subscription__order", "order", "featured", "-updated"]

    def get_checkout_url(self):
        return reverse("sub-price-checkout", kwargs={
            "price_id": self.id,
        })

    @property
    def display_description(self):
        if not self.subscription:
            return ""
        return self.subscription.description or ""

    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()

    @property
    def display_sub_name(self):
        if not self.subscription:
            return "Plan"
        return self.subscription.name

    @property
    def stripe_currency(self):
        return "eur"
    
    @property
    def stripe_price(self):
        return int(self.price * 100)

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if (not self.stripe_id and self.product_stripe_id is not None):
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval = self.interval,
                product=self.product_stripe_id,
                metadata={
                    "subscription_plan_price_id": self.id,
                }
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval
            ).exclude(id=self.id)
            qs.update(featured=False)


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    sub_stripe_id = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance 
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription

    if subscription_obj is not None:
        groups  = subscription_obj.groups.all()
        groups_ids_set = set(groups.values_list("id", flat=True))
    else:
        groups_ids_set = set()
    
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups_ids_set = set(subs_qs.values_list("groups__id", flat=True))
        current_groups_ids_set = set(user.groups.all().values_list("id", flat=True))
        user.groups.set(groups_ids_set | (current_groups_ids_set - subs_groups_ids_set))

post_save.connect(user_sub_post_save, sender=UserSubscription)
