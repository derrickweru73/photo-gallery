from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import (
    ProfileForm,
    RegistrationForm,
    UserUpdateForm,
)


def register(request):
    """Register a new user account."""

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully!"
            )

            return redirect("home")
    else:
        form = RegistrationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


class UserLoginView(LoginView):
    """Handle user login."""

    template_name = "registration/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Handle user logout."""

    next_page = reverse_lazy("home")


@login_required
def profile(request):
    """Display the logged-in user's profile."""

    return render(
        request,
        "profile.html",
    )


@login_required
def edit_profile(request):
    """Allow the logged-in user to edit their profile."""

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect("profile")

    else:
        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileForm(
            instance=request.user.profile,
        )

    return render(
        request,
        "edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


class UserPasswordChangeView(PasswordChangeView):
    """Allow users to change their password."""

    template_name = "registration/password_change.html"
    success_url = reverse_lazy("profile")
