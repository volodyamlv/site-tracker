from django.urls import path

from training import views

app_name = 'training'

urlpatterns = [
    path('', views.index, name='index')
]