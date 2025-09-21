from django.urls import path
from .views import (
    landing_page,
    dashboard_view,
   
)




urlpatterns = [
    # Landing
    path('', landing_page, name='landing'),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
]
