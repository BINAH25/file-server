from django.urls import path
from rest_api import views

app_label = "rest_api"

urlpatterns = [
    path("auth/login/", views.SignInAPI.as_view()),
    path("auth/register/", views.RegistrationAPI.as_view()),  
    path("auth/verify/", views.EmailVerificationAPI.as_view()),  
    path("auth/logout/", views.LogOutAPI.as_view()),  
    path("auth/change-password/", views.ChangePasswordAPI.as_view()),  
    path("auth/reset-password/", views.ResetPasswordAPI.as_view()),  
    path("auth/reset-password-done/", views.ResetPasswordDoneAPI.as_view()),  
    path("auth/delete-account/", views.DeleteAccountAPI.as_view()),  
]
