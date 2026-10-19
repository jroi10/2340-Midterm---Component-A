from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, MovieReview, MovieRating
from django.contrib.auth.decorators import login_required

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from cart.models import InvoiceItem

# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data["title"] = "Movies"
    template_data["movies"] = movies
    return render(request, "movies/index.html", {"template_data" : template_data})

def movie(request, id):
    movie = Movie.objects.get(id=id)
    reviews = MovieReview.objects.filter(movie=movie)
    ratings = MovieRating.objects.filter(movie=movie)

    user_rating = None
    if request.user.is_authenticated:
        user_rating = MovieRating.objects.filter(movie=movie, user=request.user).first()

    template_data = {}
    template_data["title"] = movie.name
    template_data["movie"] = movie
    template_data["reviews"] = reviews
    template_data["average_rating"] = ratings.aggregate(Avg("rating"))["rating__avg"]
    template_data["rating_count"] = ratings.count()
    template_data["user_rating"] = user_rating
    template_data["rating_options"] = [1, 2, 3, 4, 5]
    return render(request, 'movies/movie.html', {"template_data" : template_data})

@login_required
def create_review(request, id):
    if request.method == "POST" and request.POST["comment"] != "":
        movie = Movie.objects.get(id=id)
        review = MovieReview()
        review.comment = request.POST["comment"]
        review.movie = movie
        review.user = request.user
        review.save()

    return redirect("movies.movie", id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(MovieReview, id=review_id)

    if request.user != review.user:
        return redirect("movies.movie", id=id)

    if request.method == "GET":
        template_data = {}
        template_data["title"] = "Edit Review"
        template_data["review"] = review
        return render(request, "movies/edit_review.html", {"template_data": template_data})
    elif request.method == "POST" and request.POST["comment"] != "":
        review = MovieReview.objects.get(id=review_id)
        review.comment = request.POST["comment"]
        review.save()
        return redirect("movies.movie", id=id)
    else:
        return redirect("movies.movie", id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(MovieReview, id=review_id, user=request.user)
    review.delete()
    return redirect("movies.movie", id=id)

@login_required
def report_inappropriate(request, id, review_id):
    review = get_object_or_404(MovieReview, id=review_id)
    review.delete()
    return redirect("movies.movie", id=id)

@staff_member_required
def view_movie_stats(request):
    purchased_movies = Movie.objects.annotate(purchase_count=Sum("invoiceitem__quantity")).filter(purchase_count__gt=0).order_by("-purchase_count", "name")
    reviewed_movies = Movie.objects.annotate(review_count=Count("moviereview")).filter(review_count__gt=0).order_by("-review_count", "name")

    top_purchase_count = purchased_movies[0].purchase_count if purchased_movies else 0
    top_review_count = reviewed_movies[0].review_count if reviewed_movies else 0

    top_purchased_movies = [movie for movie in purchased_movies if movie.purchase_count == top_purchase_count]
    top_reviewed_movies = [movie for movie in reviewed_movies if movie.review_count == top_review_count]

    template_data = {}
    template_data["title"] = "Movie Stats"
    template_data["purchased_movies"] = purchased_movies
    template_data["reviewed_movies"] = reviewed_movies
    template_data["top_purchase_count"] = top_purchase_count
    template_data["top_review_count"] = top_review_count
    template_data["top_purchased_movies"] = top_purchased_movies
    template_data["top_reviewed_movies"] = top_reviewed_movies

    return render(request, "admin/movies/top_review_purchase.html", {**admin.site.each_context(request), "title": "Movie Stats", "template_data": template_data})

@login_required
def rate_movie(request, id):
    if request.method == "POST" and request.POST["rating"] in ["1", "2", "3", "4", "5"]:
        movie = Movie.objects.get(id=id)
        rating = MovieRating.objects.filter(movie=movie, user=request.user).first()
        if rating is None:
            rating = MovieRating()
            rating.movie = movie
            rating.user = request.user
        rating.rating = int(request.POST["rating"])
        rating.save()
    
    return redirect("movies.movie", id=id)
