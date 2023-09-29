from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from .models import Recipe, Rating
from .forms import CommentForm, RecipeForm


class RecipeList(generic.ListView):
    """
    Displays recipes on the home page that have been both approved by an admin
    and submitted by the recipe author
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4


class RecipePage(View):
    """
    Displays a recipe selected by the user, which can be commented and rated
    """

    def get(self, request, slug, *args, **kwargs):
        """
        Retrieves a user selected recipe from the database
        """
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        if request.user.is_authenticated:
            rating = Rating.objects.filter(
                recipe=recipe, user=request.user).first()
        else:
            rating = 0
        recipe.user_rating = rating.rating if rating else 0

        return render(
            request,
            "recipe_page.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "rating": rating,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        When a POST method is requested via the user comment section
        this function is called
        """
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        if request.user.is_authenticated:
            rating = Rating.objects.filter(
                recipe=recipe, user=request.user).first()
        else:
            rating = 0
        recipe.user_rating = rating.rating if rating else 0

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()
        return render(
            request,
            "recipe_page.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "rating": rating,
                "comment_form": CommentForm(),
            }
        )


class AddRecipePage(generic.CreateView):
    """
    This view allows a user to add their own recipe to the database
    """
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    success_message = _(
        'Your recipe has been successfully submitted and is awaiting approval')
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        """
        If a correctly filled in form has been successfully submitted
        to the database, this function is called and the user is returned to
        the my_recipes page
        """
        form.instance.author_id = self.request.user.id
        form.instance.slug = slugify(form.instance.title, allow_unicode=False)
        form.instance.status = 0
        super(AddRecipePage, self).form_valid(form)
        return redirect('my_recipes')


class MyRecipesList(generic.ListView):
    """
    This view allows for the user to see a list of their submitted recipes,
    and see whether they have been submitted and approved.
    """
    model = Recipe
    template_name = 'my_recipes.html'
    paginate_by = 9
    context_object_name = 'recipes'

    def get_queryset(self):
        """
        This function filters the recipes that have been added to the database
        by the user
        """
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(author=self.request.user).order_by(
                'title')
        else:
            return []


class UpdateRecipePage(generic.UpdateView):
    """
    This view allows for the user to update their draft or submitted recipes.
    An updated recipe is always reset to unapproved, even
    if previously approved by an admin.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        """
        If a correctly filled in form has been successfully submitted
        to the database, this function is called and the recipe's approved and
        published status are reset to False and 0 respectively.
        The user will then be redirected to the my_recipes page.
        """
        form.instance.author_id = self.request.user.id
        form.instance.slug = slugify(form.instance.title, allow_unicode=False)
        form.instance.approved = False
        form.instance.status = 0
        super(UpdateRecipePage, self).form_valid(form)
        return redirect('my_recipes')


class SubmitRecipePage(generic.UpdateView):
    """
    This view allows for the user to
    confirm the submission of one of their previously added recipes
    """
    model = Recipe
    fields = []
    template_name = 'submit_recipe.html'
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        """
        Once the user clicks on the submit button, their recipe's published
        status will be set to one. If the recipe is already approved, it will
        be visible to the public.
        """
        form.instance.status = 1
        super(SubmitRecipePage, self).form_valid(form)
        return redirect('my_recipes')


class DeleteRecipePage(generic.DeleteView):
    """
    This view allows for the user to
    confirm the deletion of one of their added recipes
    """
    model = Recipe
    fields = []
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('my_recipes')

    def form_valid(self, form):
        """
        Once the user clicks on the delete button, their recipe will be
        removed from the database.
        """
        super(DeleteRecipePage, self).form_valid(form)
        return redirect('my_recipes')


class CategoryPage(generic.ListView):
    """
    This view displays a list of published and approved recipes of a specific
    category as requested by the user.
    """

    def get(self, request, recipe_category, *args, **kwargs):
        """
        This function gets all recipes in the database that have a recipe
        category matching the user's request
        """
        query = recipe_category.replace("-", " ").title()
        queryset = Recipe.objects.filter(
            status=1, approved=True, recipe_category=query).order_by(
                '-created_on')
        return render(
            request,
            "index.html",
            {
                "recipe_list": queryset,
                "recipe_category": query,
            }
        )


def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    """
    This function allows for the user to post a recipe a 5 star rating, which
    contributes to the recipe's average rating
    """
    recipe = Recipe.objects.get(id=post_id)
    Rating.objects.filter(recipe=recipe, user=request.user).delete()
    recipe.rating_set.create(user=request.user, rating=rating)
    return request


def handler404(request, *args, **argv):
    """
    Handles HTTP 404 errors
    """
    return render(request, 'templates/404.html')


def handler500(request, *args, **argv):
    """
    Handles HTTP 500 errors
    """

    return render(request, 'templates/500.html')
