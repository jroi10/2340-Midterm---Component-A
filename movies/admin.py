from django.contrib import admin
from .models import Movie, MovieReview

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    search_fields = ["name"]

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieReview)