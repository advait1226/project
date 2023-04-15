from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name= 'home'),
    path('twostep/', views.two_step_option_price_view, name= 'two-step'),
    path('nstepwithvolatility/', views.n_step_option_price_volatility_view, name= 'n-step-v'),
    path('nstep/', views.n_step_option_price_view, name= 'n-step'),
    path('result/', views.result_view, name= 'result'),
    path('blacksch/', views.black_view, name= 'black'),

]