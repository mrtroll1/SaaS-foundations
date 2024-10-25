from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def profile_list_view(request):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }

    return render(request, "profiles/list.html", context)

@login_required
def profile_detail_view(request, username=None):
    user = request.user
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = profile_user_obj == user

    context = {
        "object_list": profile_user_obj,
        "instance": profile_user_obj,
        "owner": is_me,
        "sub_plan": None
    }

    # user_groups = profile_user_obj.groups.all()
    # if user_groups.filter(name__icontains="basic").exists():
    #     context['sub_plan'] = 'Basic'

    if profile_user_obj.has_perm("subscriptions.basic"):
        context['sub_plan'] = 'Basic'

    return render(request, "profiles/detail.html", context)

# @login_required
# def profile_view(request, username=None, *args, **kwargs):
#     user = request.user
#     # profile_user_obj = User.objects.get(username=username)

#     # print(user.has_perm("auth.view_user"))

#     # <app_label>.<method>_<model>, ex. auth.view_user or visits.add_pagevisit

#     profile_user_obj = get_object_or_404(User, username=username)

#     is_me = profile_user_obj == user
#     if is_me or user.is_superuser:
#         return HttpResponse(f"Hello there, {username} - {profile_user_obj.id} - {user.id}!")
#     else:
#         return render(request, "no-permission.html", {})

