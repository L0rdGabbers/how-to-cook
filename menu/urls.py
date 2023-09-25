from . import views
from django.urls import path

urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('add-recipe/', views.AddRecipePage.as_view(), name='add_recipe'),
    path('my-recipes/', views.MyRecipesList.as_view(), name='my_recipes'),
    path('update/<slug:slug>/', views.UpdateRecipePage.as_view(), name='update_recipe'),
    path('submit/<slug:slug>/', views.SubmitRecipePage.as_view(), name='submit_recipe'),
    path('delete/<slug:slug>/', views.DeleteRecipePage.as_view(), name='delete_recipe'),
    path('category/<str:recipe_category>/',
         views.CategoryPage.as_view(), name='category'),
    path('rate/<int:post_id>/<int:rating>/', views.rate),
    path('<slug:slug>/', views.RecipePage.as_view(), name='recipe_page'),
]
