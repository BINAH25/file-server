from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("register", views.Register.as_view(), name="register"),
    path("verify", views.CodeVerificationView.as_view(), name="verify"),
    path("log-out", views.LogoutView.as_view(), name="log-out"),

]
