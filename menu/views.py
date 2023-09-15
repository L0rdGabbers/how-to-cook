from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Recipe
from .forms import CommentForm, RecipeForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class RecipePage(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        rated = False
        if recipe.star_rating.filter(id=self.request.user.id).exists():
            rated = True

        return render(
            request,
            "recipe_page.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "rated": rated,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        rated = False
        if recipe.star_rating.filter(id=self.request.user.id).exists():
            rated = True

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
            "add_recipe.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "rated": rated,
                "comment_form": CommentForm()
            },
        )


class AddRecipePage(generic.CreateView):
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    success_url = reverse_lazy('home')
    success_message = (
        'Your recipe has been successfully submitted and is awaiting approval')
    title = 'Add a job'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.slug = slugify(form.instance.title, allow_unicode=False)
        form.instance.status = 1
        form.instance.featured_image.url = ""
        super(AddRecipePage, self).form_valid(form)
        return redirect('add_recipe')


class MyRecipesList(generic.ListView):
    model = Recipe
    template_name = 'my_recipes.html'
    paginate_by = 6
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
