from django.shortcuts import render
from visits.models import PageVisit

from dashboard.views import dashboard_view

# Create your views here.
def landind_page_view(request):
    if request.user.is_authenticated:
        return dashboard_view(request) # do not do smth like this often
    qs_count = PageVisit.objects.all().count()
    context = {
        "total_visit_count": qs_count
    }
    PageVisit.objects.create(path=request.path)
    return render(request, "landing/main.html", context=context)