from .models import Comment, Recipe
from django import forms
from django_summernote.widgets import SummernoteWidget


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
