from django.shortcuts import render
from visits.models import PageVisit

# Create your views here.
def landind_page_view(request):
    qs_count = PageVisit.objects.all().count()
    context = {
        "total_visit_count": qs_count
    }
    PageVisit.objects.create(path=request.path)
    return render(request, "landing/main.html", context=context)