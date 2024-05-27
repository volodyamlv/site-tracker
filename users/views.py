from turtle import title
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import context
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("main:index"))
        else:
            messages.error(request, 'Неправильный логин или пароль.')

    else:
        form = UserLoginForm()
    context = {"title": "Вход", "form": form}
    return render(request, "users/login.html", context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("main:index"))


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {"title": "Регистрация", "form": form}
    return render(request, "users/registration.html", context)

@login_required
def profile(request):
    context = {
        "title": "Профиль",
    }
    return render(request, "users/profile.html", context)
