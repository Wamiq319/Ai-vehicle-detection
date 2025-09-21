from django.urls import path
from . import views

app_name = "tolls"

urlpatterns = [
    path('rates/', views.toll_rates_view, name='toll_rates'),
]
