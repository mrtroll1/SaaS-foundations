from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission
from django.conf import settings

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
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS],
    })

    def __str__(self):
        return f'{self.name}'

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
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
