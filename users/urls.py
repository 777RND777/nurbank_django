from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),

    path("login/", views.LogIn.as_view(), name="log_in"),
    path("logout/", views.LogOut.as_view(), name="log_out"),
    path("register/", views.Register.as_view(), name="register"),

    path("users/", views.UserList.as_view(), name="user_list"),
    path("users/<slug:slug>/", views.UserDetail.as_view(), name="user_detail"),
]
