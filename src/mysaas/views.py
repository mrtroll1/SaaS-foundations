from django.http import HttpResponse
from django.shortcuts import render, redirect
from visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

LOGIN_URL = settings.LOGIN_URL

def home_view(request, *args, **kwargs):
    return about_view(request, *args, **kwargs)

def about_view(request):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try: 
        percent = round((page_qs.count() * 100.0) / qs.count(), 2)
    except:
        percent = 0
    my_title = "Title"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count()
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

def contact_view(request):
    return render(request, 'contact/contact.html')

VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get("protected_page_allowed") or 0

    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent==VALID_CODE:
            request.session['protected_page_allowed'] = 1
            is_allowed = True

    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})

@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    # if not request.user.is_authenticated():
    #     return redirect('/accounts/login')

    return render(request, "protected/user-only.html", {})

@staff_member_required(login_url='/no-permission/')
def staff_only_view(request, *args, **kwargs):

    return render(request, "protected/staff-only.html", {})

def no_permission_view(request):
    if request.user.is_authenticated:
        return render(request, 'no-permission.html')
    else:
        return redirect('account_login')

def old_home_page_view(request, *args, **kwargs):
    my_title = "Native python methods"
    my_context = {
        "page_title": my_title
    }
    html_ = """
    <!DOCTYPE html>
    <html>
        <body>
            <h1>is {page_title} anything?</h1>
        </body>
    <html>
""".format(**my_context)
    return HttpResponse(html_)