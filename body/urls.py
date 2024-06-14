from django.urls import path
from django.contrib.auth.decorators import login_required

from body import views

app_name = 'body'

urlpatterns = [
    path('', login_required(views.body_view), name='body_view'),
]