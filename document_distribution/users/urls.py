from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("register", views.Register.as_view(), name="register"),
    path("verify", views.CodeVerificationView.as_view(), name="verify"),
    path("log-out", views.LogoutView.as_view(), name="log-out"),
    path("reset_password", views.ResetPasswordView.as_view(), name="reset_password"),
    path("password_reset_done", views.PasswordResetDone.as_view(), name="password_reset_done"),
    path("delete-account", views.DeleteAccount.as_view(), name="delete-account"),
]
