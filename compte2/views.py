from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from compte.forms import CreerUser
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
#@login_required(login_url = 'acces')
# inscription
def inscripage2(request) :
    form =  CreerUser()
    if request.method=='POST' :
        form = CreerUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Compte creé avec succes pour ' + user)
            return redirect('acces2')
    context = {'form' : form}
    return render(request, 'compte2\inscrit.html', context)
# connection
def accespage2(request) :
    context = {}
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None :
            login(request, user)
            return redirect('/admin/')
        else :
            messages.info(request, "il ya une erreur sur le mot de passe ou nom d'utilisateur")
        
    return render(request, 'compte2\login.html')
#logout
def lagoutuser2(request):
    logout(request)
    return redirect('acces')