from django.urls import path

from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),

    path("login/", LogIn.as_view(), name="log_in"),
    path("logout/", LogOut.as_view(), name="log_out"),
    path("register/", Register.as_view(), name="register"),

    path("users/", UserList.as_view(), name="user_list"),
    path("users/<slug:slug>", UserDetail.as_view(), name="user"),
]
