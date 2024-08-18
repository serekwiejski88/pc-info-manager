from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recive_data/', views.receive_data, name='receive_data'),
    path('<str:mac_address>/', views.pc, name='pc'),
]