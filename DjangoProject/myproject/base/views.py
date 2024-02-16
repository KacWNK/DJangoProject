from django.shortcuts import render, redirect
from django.urls import reverse
from pyexpat.errors import messages
from .models import Availability, Tcourt
from .models import Room, User
from .forms import AvailabilityForm, UserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse


# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not match')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An Error Occured')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    rooms = Room.objects.all()
    return render(request, 'base/home.html', {'rooms': rooms})


def room(request, prim):
    room = Room.objects.get(id=prim)
    selected_level = request.GET.get('q', None)
    users = User.objects.all().order_by('-level')
    search_query = request.GET.get('search', None)
    distinct_levels = sorted(set(user.level for user in users), reverse=True)
    tcourts = Tcourt.objects.all()

    if selected_level:

        availabilities = Availability.objects.filter(user__level=selected_level)
    else:

        availabilities = Availability.objects.all()
    if search_query:
        availabilities = availabilities.filter(
            Q(day__icontains=search_query) | Q(user__name__icontains=search_query) | Q(
                user__age__icontains=search_query)
        )
        search_query = ""
    else:
        search_query = ""

    context = {'room': room, 'availabilities': availabilities, 'users': users, 'search_query': search_query,
               'distinct_levels': distinct_levels, 'tcourts': tcourts}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createChallenge(request):
    form = AvailabilityForm(user=request.user)
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, user = request.user )
        if form.is_valid():
            form.save()
            return redirect('room/2')
    context = {'form': form}
    return render(request, 'base/forms.html', context)


@login_required(login_url='login')
def updateChallenge(request, prim):
    availabilities = Availability.objects.get(id=prim)
    form = AvailabilityForm(instance=availabilities)

    if request.user != availabilities.user:

        messages.error(request, 'You are not authorized to')
        return redirect(reverse('room', kwargs={'prim': 2}))

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availabilities)
        if form.is_valid():
            form.save()
            return redirect(reverse('room', kwargs={'prim': 2}))
    context = {'form': form}
    return render(request, 'base/forms.html', context)


@login_required(login_url='login')
def deleteChallenge(request, prim):
    availabilities = Availability.objects.get(id=prim)

    if request.user != availabilities.user:
        messages.error(request, 'You are not authorized to')
        return redirect(reverse('room', kwargs={'prim': 2}))

    if request.method == 'POST':
        availabilities.delete()
        return redirect(reverse('room', kwargs={'prim': 2}))
    return render(request, 'base/delete.html', {'object': availabilities})

def resetPassword(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            messages.success(request, f'A reset password email has been sent to {email}')
        except Exception as e:
            messages.error(request, 'No user with that email')

    return render(request, 'base/reset_password.html')

