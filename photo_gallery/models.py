from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Store additional information for each user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    """Represent a tag that can be assigned to photos."""

    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Represent a photo uploaded to the gallery."""

    title = models.CharField(
        max_length=200
    )
    description = models.TextField(
        blank=True
    )
    image = models.ImageField(
        upload_to="photos/"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="photos"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PhotoInteraction(models.Model):
    """Store a user's like or dislike for a photo."""

    LIKE = "like"
    DISLIKE = "dislike"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="photo_interactions"
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="interactions"
    )
    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "photo"],
                name="unique_user_photo_interaction"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.photo.title} - {self.reaction}"
