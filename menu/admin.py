from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
import random
from .models import Recipe, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    summernote_fields = ('summary', 'instructions')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    search_fields = ['title', 'summary']
    actions = ['approve_recipies']

    def approve_recipies(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'rating')
    list_filter = ('recipe', 'rating')
    search_fields = ['user__username', 'recipe__title',]
