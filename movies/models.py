from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + " - " + self.name

class MovieReview(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " - " + self.movie.name

class TopCommenter(User):
    class Meta:
        proxy = True
        verbose_name = "Top Commenter"
        verbose_name_plural = "Top Commenters"

class MovieRating(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " - " + self.movie.name + " - " + str(self.rating)
