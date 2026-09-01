from django.contrib import admin

from .models import Photo, PhotoInteraction, Profile, Tag


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_by", "created_at")
    list_filter = ("tags", "created_at")
    search_fields = ("title", "description")
    filter_horizontal = ("tags",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(PhotoInteraction)
class PhotoInteractionAdmin(admin.ModelAdmin):
    list_display = ("user", "photo", "reaction", "created_at")
    list_filter = ("reaction", "created_at")
    search_fields = ("user__username", "photo__title")