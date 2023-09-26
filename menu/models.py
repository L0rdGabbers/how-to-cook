from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from statistics import mean

STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"
    STARTERS = "Starters"
    CAKES = "Cakes"
    DESSERTS = "Desserts"
    BREAD = "Bread"
    VEGETARIAN = "Vegetarian"
    BEVERAGES = "Beverages"
    PASTA = "Pasta"
    OVEN_MEALS = "Oven Meals"
    EASTERN_FOOD = "Eastern Food"
    QUICK_MEALS = "Quick Meals"
    OTHER = "Other"
    DIFFICULTY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (EXPERT, "Expert")
    ]
    RECIPE_CATEGORIES = [
        (STARTERS, "Starters"),
        (BREAD, "Bread"),
        (VEGETARIAN, "Vegetarian"),
        (PASTA, "Pasta"),
        (OVEN_MEALS, "Oven Meals"),
        (EASTERN_FOOD, "Eastern Food"),
        (QUICK_MEALS, "Quick Meals"),
        (BEVERAGES, "Beverages"),
        (DESSERTS, "Desserts"),
        (CAKES, "Cakes"),
        (OTHER, "Other")
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
    time_to_prepare = models.PositiveIntegerField()
    recipe_category = models.CharField(
        max_length=20, choices=RECIPE_CATEGORIES, default='QUICK_MEALS'
    )
    difficulty = models.CharField(
        max_length=12, choices=DIFFICULTY_CHOICES, default=BEGINNER)
    portions = models.PositiveIntegerField(default=1)
    ingredients = models.TextField()
    instructions = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def average_star_rating(self) -> float:
        return Rating.objects.filter(recipe=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.title}"

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.recipe}: {self.rating} by {self.user}"