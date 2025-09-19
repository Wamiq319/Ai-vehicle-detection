from django.urls import path
from .views import (
    landing_page,
    login_page,
   
)




urlpatterns = [
    # Landing & Authentication
    path('', landing_page, name='landing'),
    path('login/', login_page, name='login'),
]
