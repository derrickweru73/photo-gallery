from django.urls import path
from .views import upload_photo
from .views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    edit_profile,
    home,
    interact_with_photo,
    photo_detail,
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
    "photo/<int:pk>/",
    photo_detail,
    name="photo_detail",
    ),

    path(
    "photo/<int:pk>/like/",
    interact_with_photo,
    {
        "reaction": "like",
    },
    name="photo_like",
    ),

    path(
        "photo/<int:pk>/dislike/",
        interact_with_photo,
        {
            "reaction": "dislike",
        },
        name="photo_dislike",
    ),


    path("upload/", upload_photo, name="upload_photo"),


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