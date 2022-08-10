from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("login/", LogInView.as_view(), name="log_in"),
    path("logout/", LogOutView.as_view(), name="log_out"),
    path("register/", RegisterView.as_view(), name="register"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<slug:slug>", UserDetailView.as_view(), name="user"),
]
