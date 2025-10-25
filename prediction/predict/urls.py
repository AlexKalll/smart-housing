from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_price, name='predict_price'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]