from typing import Any
from django.conf import settings
from django.db.models import Q

from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
from customers.models import Customer
import helpers.billing

def refresh_users_subscription(
        user_ids=None, active_only=True, 
        verbose=True, days_ago=0, days_left=0,
        day_start=-1, day_end=-1):
    if active_only:
        qs = UserSubscription.objects.all().by_active()
    else:
        qs = UserSubscription.objects.all()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    if days_ago > 0:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > 0:
        qs = qs.by_days_left(days_left=days_left)
    if day_start > -1 and day_end >= day_start:
        qs = qs.by_range(day_start=day_start, day_end=day_end)
    
    complete_count = 0
    qs_count = qs.count()
    for obj in qs:
        if obj.sub_stripe_id:
            user = obj.user
            if verbose:
                print(f'Syncing {user} active subs')
            sub_data = helpers.billing.get_subscription(obj.sub_stripe_id, raw=False)
        for k, v in sub_data.items():
            setattr(obj, k, v)
        obj.save()
        complete_count += 1
    
    return complete_count == qs_count

def clear_dangling_subs(verbose=True):
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for obj in qs:
        user = obj.user
        customer_stripe_id = obj.stripe_id
        if verbose:
            print(f'Removing {user} - {customer_stripe_id} old subs')
        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            db_user_subs = UserSubscription.objects.filter(
                sub_stripe_id__iexact=f'{sub.id}'.strip()
            )
            if db_user_subs.exists():
                continue
            else:
                helpers.billing.cancel_subscription(
                    stripe_id=sub.id, 
                    cancel_at_period_end=True,
                    reason="Was an active dangling subscription.", 
                    raw=True 
                )

def sync_sub_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)