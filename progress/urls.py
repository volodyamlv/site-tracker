from django.urls import path

from progress import views

app_name = 'progress'

urlpatterns = [
    path('', views.index, name='index'),
]