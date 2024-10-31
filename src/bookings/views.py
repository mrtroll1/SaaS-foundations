from django.shortcuts import render
from .forms import BookingForm

# Create your views here
def booking_form_view(request, *args, **kwargs):
    form = BookingForm()
    context = {'form': form}

    return render(request, 'bookings/main.html', context=context)

def booking_confirmation_view(request, *args, **kwargs):

    return render(request, 'bookings/confirmation.html')