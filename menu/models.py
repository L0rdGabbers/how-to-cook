from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from statistics import mean

STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"
    DIFFICULTY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (EXPERT, "Expert")
    ]
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe_posts")
    updated_on = models.DateTimeField(auto_now=True)
    summary = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='placeholder', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    star_rating = models.ManyToManyField(
        User, related_name="recipe_rating", blank=True)
    time_to_prepare = models.PositiveIntegerField()
    difficulty = models.CharField(
        max_length=12, choices=DIFFICULTY_CHOICES, default=BEGINNER)
    ingredients = models.TextField()
    instructions = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def ingredients_list(self):
        return self.ingredients.split(",")


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Rating(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='rating')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    score = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Star rating {self.score} by {self.name}"

    def rating(self):
        return round(sum(recipe.star_rating.values) / len(recipe.star_rating.values), 0)
