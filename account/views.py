from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
# Create your views here.


def sing_out(request):
    logout(request)
    return redirect('/')


def sing_in(request):
    form = UserSingInForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get['username']
        password = form.cleaned_data.get['password']

        user = authenticate(username=username, password=password)

        login(request, user)
        return redirect('/')

    context = {
        'form': form,
        'f': 'sing in',
    }
    return render(request, 'Sing.html', context)


def sing_up(request):
    form = UserSingUpForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get['password']
        user.set_password = password
        user.sava()
        new_user = authenticate(username=user.usernaem, password=password)

        return redirect('/')

    context= {
        'form': form,
        'f': 'sing up'
    }
    return render(request, 'Sing.html', context)