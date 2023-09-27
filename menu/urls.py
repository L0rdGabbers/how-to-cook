from . import views
from django.urls import path

urlpatterns = [
    # Path to the home page
    path('', views.RecipeList.as_view(), name='home'),

    # Path to the add recipe page
    path('add-recipe/', views.AddRecipePage.as_view(), name='add_recipe'),

    # Path to the my recipes page
    path('my-recipes/', views.MyRecipesList.as_view(), name='my_recipes'),
    
    # Path to a update recipe page, which pases the recipe's slug into the url
    path('update/<slug:slug>/',
         views.UpdateRecipePage.as_view(), name='update_recipe'),
    
    # Path to a submit recipe page, which pases the recipe's slug into the url
    path('submit/<slug:slug>/',
         views.SubmitRecipePage.as_view(), name='submit_recipe'),

    # Path to a delete recipe page, which pases the recipe's slug into the url
    path('delete/<slug:slug>/',
         views.DeleteRecipePage.as_view(), name='delete_recipe'),

    # Path to category page, which pases a category string into the url
    path('category/<str:recipe_category>/',
         views.CategoryPage.as_view(), name='category'),

    # Path to the rate function which posts a user's recipe rating to the db
    path('rate/<int:post_id>/<int:rating>/', views.rate),

    # Path to a recipe's main page, passing the recipe's slug into the url
    path('<slug:slug>/', views.RecipePage.as_view(), name='recipe_page'),
]
