from django.urls import path

from training import views

app_name = 'training'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('<int:pk>/', views.template_detail, name='template_detail'),
    path('template/delete/<int:pk>/', views.template_delete, name='template_delete'),
    # path('/exercise/<int:pk>', views.exercise, name='exercise'),
]