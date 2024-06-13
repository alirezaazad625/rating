from django.contrib import admin

from .models import Rating, PostRating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rating._meta.get_fields()]
    search_fields = [field.name for field in Rating._meta.get_fields()]


@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostRating._meta.get_fields()]
    search_fields = [field.name for field in PostRating._meta.get_fields()]
