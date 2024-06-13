from django.urls import path
from django.contrib.auth.decorators import login_required

from history import views

app_name = 'history'

urlpatterns = [
    path('', login_required(views.history_list), name='history_list'),
    path('<str:template_name>/<str:date>/', views.detail, name='detail'),
]