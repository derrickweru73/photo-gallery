from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse_lazy
from .forms import PhotoForm
from .forms import (
    ProfileForm,
    RegistrationForm,
    UserUpdateForm,
)

from .models import Photo, PhotoInteraction, Tag



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

def home(request):
    """Display photos on the gallery homepage."""

    photos = Photo.objects.all()

    selected_tag = request.GET.get("tag")

    if selected_tag:
        photos = photos.filter(
            tags__name=selected_tag
        )

    tags = Tag.objects.all()

    return render(
        request,
        "home.html",
        {
            "photos": photos,
            "tags": tags,
            "selected_tag": selected_tag,
        },
    )

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    like_count = photo.interactions.filter(
        reaction=PhotoInteraction.LIKE
    ).count()

    dislike_count = photo.interactions.filter(
        reaction=PhotoInteraction.DISLIKE
    ).count()

    return render(
        request,
        "photo_detail.html",
        {
            "photo": photo,
            "like_count": like_count,
            "dislike_count": dislike_count,
        },
    )

@login_required
def interact_with_photo(request, pk, reaction):
    """Create or update a user's reaction to a photo."""

    photo = get_object_or_404(
        Photo,
        pk=pk,
    )

    if reaction not in (
        PhotoInteraction.LIKE,
        PhotoInteraction.DISLIKE,
    ):
        return redirect("photo_detail", pk=photo.pk)

    PhotoInteraction.objects.update_or_create(
        user=request.user,
        photo=photo,
        defaults={
            "reaction": reaction,
        },
    )

    return redirect("photo_detail", pk=photo.pk)

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

@login_required
def upload_photo(request):
    """Allow logged-in users to upload a photo."""

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            form.save_m2m()

            return redirect("photo_detail", pk=photo.pk)
    else:
        form = PhotoForm()

    return render(
        request,
        "upload_photo.html",
        {"form": form},
    )

class UserPasswordChangeView(PasswordChangeView):
    """Allow users to change their password."""

    template_name = "registration/password_change.html"
    success_url = reverse_lazy("profile")
