from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = self.request.POST['username']
            password = self.request.POST['password1']

            user = authenticate(username=username, password=password)
            login(self.request, user)

            return redirect("/")
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {"form": form})


def user_account(request):
    return render(request, 'users/user_account.html')
