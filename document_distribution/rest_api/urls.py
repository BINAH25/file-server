from django.urls import path
from rest_api import views

app_label = "rest_api"

urlpatterns = [
    # USER URLS
    path("auth/login/", views.SignInAPI.as_view()),
    path("auth/register/", views.RegistrationAPI.as_view()),  
    path("auth/verify/", views.EmailVerificationAPI.as_view()),  
    path("auth/logout/", views.LogOutAPI.as_view()),  
    path("auth/change-password/", views.ChangePasswordAPI.as_view()),  
    path("auth/reset-password/", views.ResetPasswordAPI.as_view()),  
    path("auth/reset-password-done/", views.ResetPasswordDoneAPI.as_view()),  
    path("auth/delete-account/", views.DeleteAccountAPI.as_view()),  
    # FILE URLS
    path("file/upload-file/", views.UploadFileAPI.as_view()),  
    path("file/get-all-files/", views.GetAllFilesAPI.as_view()),  
    path("file/delete-file/<int:pk>/", views.DeleteFileAPI.as_view()),  
    path("file/download-file/<int:pk>/", views.DownloadFileAPI.as_view()),  
    path("file/search-file/", views.SearchFileAPI.as_view()),  
    path("file/get-file/<int:pk>/", views.GetFile.as_view()),  
    path("file/send-file-via-email/", views.SendFileViaEmailAPI.as_view()),  
    
]
