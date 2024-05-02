from django.urls import path
from rest_api import views

app_label = "rest_api"

urlpatterns = [
    path("auth/login/", views.SignInView.as_view()),
    path("auth/register/", views.RegistrationView.as_view()),  
    path("auth/verify/", views.EmailVerificationView.as_view()),  
    path("auth/logout/", views.LogOutView.as_view()),  
]
