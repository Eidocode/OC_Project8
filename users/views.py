from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {"form": form})


def user_account(request):
    return render(request, 'users/user_account.html')
