from django.urls import path
from django.contrib.auth.decorators import login_required

from training import views

app_name = 'training'

urlpatterns = [
    path('', login_required(views.template_list), name='template_list'),
    path('create/', login_required(views.template_create), name='template_create'),
    path('template/delete/<int:pk>/', login_required(views.template_delete), name='template_delete'),
    path('<int:pk>/', login_required(views.exercise_form), name='exercise_form'),
    # path('/exercise/<int:pk>', views.exercise, name='exercise'),
]