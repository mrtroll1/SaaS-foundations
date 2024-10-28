from django.shortcuts import render,  redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from subscriptions.models import SubscriptionPrice, UserSubscription
import helpers.billing
from subscriptions import utils as subs_utils

# Create your views here.
@login_required
def user_subscription_view(request, *args, **kwargs):
    _user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    # context = _user_sub_obj.serialize()
    if request.method == "POST":
        finished = subs_utils.refresh_users_subscription(user_ids=[request.user.id], active_only=False)
        if finished:
            messages.success(request, "Your plan details have been refreshed")
        else:
            messages.error(request, "Your plan details have not been refreshed, please try again")
        return redirect(_user_sub_obj.get_absolute_url())
    
    return render(request, 'subscriptions/user-detail-view.html', {"subscription": _user_sub_obj})

@login_required
def user_subscription_cancel_view(request, *args, **kwargs):
    _user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    # context = _user_sub_obj.serialize()
    if request.method == "POST":
        if _user_sub_obj.sub_stripe_id and _user_sub_obj.is_active_status:
            sub_data = helpers.billing.cancel_subscription(_user_sub_obj.sub_stripe_id, cancel_at_period_end=True, reason="User wanted to end.", feedback="other", raw=False)
        for k, v in sub_data.items():
            setattr(_user_sub_obj, k, v)
        _user_sub_obj.save()
        messages.success(request, "Your plan has been canceled")
        return redirect(_user_sub_obj.get_absolute_url())
    
    return render(request, 'subscriptions/user-cancel-view.html', {"subscription": _user_sub_obj})

def subscription_price_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY

    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": inv_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": inv_yr})

    active = inv_mo
    object_list = qs.filter(interval=inv_mo)
    if interval == inv_yr:
        active = inv_yr
        object_list = qs.filter(interval=inv_yr)

    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "mo_url": mo_url,
        "yr_url": yr_url,
        "active": active,
    })