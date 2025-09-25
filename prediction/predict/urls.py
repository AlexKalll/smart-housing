from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pr/', views.predict_price, name='predict_price'),
]