from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
    path('convert-token/', views.convert_token),
    path('goog/', views.check_google_login),
]