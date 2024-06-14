from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Body
from .forms import BodyForm
from django.urls import reverse

def body_view(request):
    body_data = Body.objects.filter(user=request.user).order_by("-date_created")

    if request.method == "POST":
        form = BodyForm(request.POST)
        if form.is_valid():
            body_measurement = form.save(commit=False)
            body_measurement.user = request.user
            body_measurement.save()
            return redirect("body:body_view")
    else:
        form = BodyForm()

    context = {
        "body_data": body_data,
        "form": form,
    }
    return render(request, "body/body.html", context)


