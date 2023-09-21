from .models import Comment, Recipe, Rating
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'summary', 'featured_image', 'time_to_prepare',
                  'difficulty', 'ingredients', 'instructions',)
        widgets = {
            'instructions': SummernoteWidget()
        }
        labels = {
            'title': _('Recipe Title'),
            'summary': _('Recipe Summary'),
            'featured_image': _('Image'),
            'time_to_prepare': _('Time to prepare (in minutes)')
        }

class StarRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score',)
