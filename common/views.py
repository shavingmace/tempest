from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm

# Create your views here.

def signup(req):
    if req.method == "POST":
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(req, 'common/signup.html', {'form': form})