from django.urls import path

from food import views

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_food/', views.search_food, name='search_food'),
]