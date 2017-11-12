from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def loginPage(request):
    return render(request, "login/login.html")
def registration(request):
    request.session.success = None
    return render(request, "login/registration.html")
def register(request):
    response = User.objects.add_user(request.POST)
    if not response ['status']:
        for error in response['error']:
            messages.error(request, error)
        return redirect('login/registration')
    messages.success(request, "You have registered succesfully")
    request.session['error'] = False
    return redirect('login/loginPage')
def login(request):
    response = User.objects.login_user(request.POST)
    request.session['error'] = False
    if not response['status']:
        for error in response['error']:
            messages.error(request, error)
            request.session['error'] = True
        return redirect('login/loginPage')
    request.session['currentUser']=response['user'][0].email
    return redirect('/')
