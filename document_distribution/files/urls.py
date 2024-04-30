from django.urls import path
from . import views

app_name = "files"

urlpatterns = [
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("file-upload", views.UploadFile.as_view(), name="file-upload"),
    path('delete/<int:pk>/', views.file_delete, name="delete"),
    path('download/<int:pk>/', views.download_file, name="download"),
    path('account', views.AccounView.as_view(), name="account"),
    path('change-password', views.ChangePasswordView.as_view(), name="change-password"),
    path("user-dashboard", views.UserDashboard.as_view(), name="user-dashboard"),
    path("user-account", views.UserAccounView.as_view(), name="user-account"),
    path("search-file", views.SearchView.as_view(), name="search-file"),
    path("send-file-via-email/<int:pk>/", views.SendFileViaEmail.as_view(), name="send-file-via-email"),

   
]
