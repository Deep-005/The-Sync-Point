from django.contrib import admin
from .models import BlogPost, Contact, Comment, CustomUser

# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    search_fields = ['title', 'author']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author_name', 'blog_post_title', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email']
    list_editable = ['is_approved']
    list_per_page = 20

    def blog_post_title(self, obj):
        return obj.blog_post.title


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'pnumber']
    search_fields = ['name', 'email']