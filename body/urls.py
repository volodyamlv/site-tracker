from django.urls import path

from body import views

app_name = 'body'

urlpatterns = [
    path('', views.index, name='index')
]