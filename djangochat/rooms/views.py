from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Room

# Create your views here.

@login_required()
def rooms(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'room/rooms.html', context=context)
