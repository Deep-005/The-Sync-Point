from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BlogPost(models.Model):
    CONTENT_TYPES = [
        ('Business', 'Business'),
        ('Travel', 'Travel'),
        ('Sports', 'Sports'),
        ('Food', 'Food'),
        ('Fashion', 'Fashion'),
        ('Technology', 'Technology'),
        ('Creative', 'Creative'),
        ('Health', 'Health'),
        ('Entertainment', 'Entertainment'),
    ]
    
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)

    author = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    image = models.ImageField(upload_to='blog_images/')  
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    spotlight = models.BooleanField(default=False, help_text="Featured in spotlight section")
    editors_choice = models.BooleanField(default=False, help_text="Selected by editors")
    featured = models.BooleanField(default=False, help_text="Featured on homepage")
    likes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    dislikes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    views = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.title}'
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save()
    
    def add_like(self):
        """Add a like"""
        self.likes += 1
        self.save()
    
    def add_dislike(self):
        """Add a dislike"""
        self.dislikes += 1
        self.save()

    def _format_number(self, num):
        """Convert number to 1.2k format"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}k"
        return str(num)
    
    @property
    def views_formatted(self):
        """Format views for display"""
        return self._format_number(self.views)
    
    @property
    def likes_formatted(self):
        """Format likes for display"""
        return self._format_number(self.likes)
    
    @property
    def dislikes_formatted(self):
        """Format dislikes for display"""
        return self._format_number(self.dislikes)
    


class Comment(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, help_text="Name of the commenter")
    author_email = models.EmailField(blank=True, help_text="Email of the commenter")
    comment_text = models.TextField(max_length=1000, help_text="The comment message")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Only approved comments are visible")

    def __str__(self):
        return f'Comment by {self.author_name} on "{self.blog_post.title[:30]}..."'

    @property
    def blog_title(self):
        """Get the blog title without querying separately"""
        return self.blog_post.title

    @property
    def formatted_date(self):
        """Get formatted date for display"""
        return self.created_at.strftime("%b %d, %Y")

    @property
    def formatted_time(self):
        """Get formatted time for display"""
        return self.created_at.strftime("%I:%M %p")




class Contact(models.Model):
    name= models.CharField(max_length=200)
    email= models.EmailField()
    pnumber = models.CharField(max_length=20, null=True, blank=True)
    message= models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class CustomUser(AbstractUser):
    # Inherits: username, email, password, first_name, last_name, etc.
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    
    # Blog relationship (No need to store list - use reverse relation)
    # We'll access user's blogs via: user.blogpost_set.all()
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username