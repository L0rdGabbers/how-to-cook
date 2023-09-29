from .models import Comment, Recipe
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    """
    A form which allows for the user to post a comment on a recipe's page
    """
    class Meta:
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):
    """
    A form which allows for the user to post a star rating, which is then
    contributed to the recipe's average star rating
    """
    class Meta:
        model = Recipe
        fields = ('title', 'summary', 'recipe_category', 'featured_image',
                  'time_to_prepare', 'difficulty',
                  'portions', 'ingredients', 'instructions',)
        widgets = {
            'instructions': SummernoteWidget()
        }
        labels = {
            'title': _('Recipe Title'),
            'summary': _('Recipe Summary'),
            'featured_image': _('Image'),
            'ingredients': _(
                'Ingredients (Please separate each item with a comma)'),
            'time_to_prepare': _('Time to prepare (in minutes)')
        }
