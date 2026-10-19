from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count
from django.template.response import TemplateResponse
from .models import Movie, MovieReview, TopCommenter, MovieRating

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    search_fields = ["name"]

class TopCommenterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
            return False

    def has_delete_permission(self, request, obj=None):
            return False

    def changelist_view(self, request, extra_context = None):
          commentors = (
                User.objects.annotate(comment_count=Count("moviereview"))
                .filter(comment_count__gt=0)
                .order_by("-comment_count", "username")
          )
          top_count = commentors[0].comment_count if commentors else 0
          top_users = [u for u in commentors if u.comment_count == top_count]

          context = {
                **self.admin_site.each_context(request),
                "title": "Top Commenters",
                "commenters": commentors,
                "top_users": top_users,
                "top_count": top_count
          }
          return TemplateResponse(request, "admin/movies/top_commenters.html", context)

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieReview)
admin.site.register(TopCommenter, TopCommenterAdmin)
admin.site.register(MovieRating)
