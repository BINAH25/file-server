from django.urls import path
from . import views

app_name = "files"

urlpatterns = [
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("file-upload", views.UploadFile.as_view(), name="file-upload"),
    path('detele/<int:pk>/', views.file_delete, name="delete"),
   
]
