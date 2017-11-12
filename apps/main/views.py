from django.shortcuts import render, redirect
from .indeedScript import parseIndeed
from .zipScript import parseZip
from django.contrib import messages
from ..login.models import User
from .models import Search

def index(request):
    try:
        request.session['currentUser']
    except:
        request.session['currentUser'] = ''
    if request.session['currentUser'] != '':
        this_user = User.objects.filter(email = request.session['currentUser'])[0]
        userSearchs = Search.objects.filter(userlist =this_user)
        context = {
            'userMessage' : "Welcome " + request.session['currentUser'],
            'userSearch' : userSearchs
                    }
    else:
        context = {
            'message' : 'Want to save your search history? Click here to login.'
        }
    return render(request,'main/index.html',context)

# Create your views here.
def refineSearch(request):
    myUrl  = request.POST['url']
    if request.POST['site'] == "Indeed":
        if request.session['currentUser']:
            response = parseIndeed(myUrl,request.session['currentUser'])
        else:
            response =  parseIndeed(myUrl)
    if request.POST['site'] == "Ziprecruiter":
        if request.session['currentUser']:
            response = parseZip(myUrl,request.session['currentUser'])
        else:
            response = parseZip(myUrl)
    if response['error_message']:
        messages.error(request, response['error_message'])
        return redirect('/')
    else:
        context = {
            'results': response['results'],
            'original': response['original'],
            'new': response['newLen']
        }
        return render(request,'main/results.html', context)
def histSearch(request, id):
    search_object = Search.objects.filter(id=id)[0]
    if "indeed" in search_object.urlText:
        response = parseIndeed(search_object.urlText)
    if "ziprecruiter" in search_object.urlText:
        response = parseZip(search_object.urlText)
    if response['error_message']:
        messages.error(request, response['error_message'])
        return redirect('/')
    else:
        context = {
            'results': response['results'],
            'original': response['original'],
            'new': response['newLen']
        }
        return render(request,'main/results.html', context)

def logout(request):
    request.session['currentUser'] = ''
    return redirect('/')
