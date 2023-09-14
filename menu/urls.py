from . import views
from django.urls import path

urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('add-recipe/', views.AddRecipePage.as_view(), name='add_recipe'),
    path('<slug:slug>/', views.RecipePage.as_view(), name='recipe_page'),
]
