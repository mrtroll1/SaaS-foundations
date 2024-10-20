from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit

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