from django.shortcuts import render, get_object_or_404
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

login_required()
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)

    context = {
        'room': room
    }
    return render(request, 'room/room_detail.html', context)
