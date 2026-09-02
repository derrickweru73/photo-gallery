from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    edit_profile,
    home,
    profile,
    register,
)


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),


    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),

    path(
        "profile/",
        profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        edit_profile,
        name="edit_profile",
    ),

    path(
        "password-change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
]