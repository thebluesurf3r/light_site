from django.urls import path
from . import views

urlpatterns = [
    path('tree', views.index, name='index'),
    path('graphs/', views.graphs, name='graphs')
]