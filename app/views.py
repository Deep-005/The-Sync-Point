from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .models import BlogPost, Contact, Comment, CustomUser
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging
from django.db.models import Sum


# Page views
def home(request):
    posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    spotlight = BlogPost.objects.filter(spotlight=True, status='published')
    editors_choice = BlogPost.objects.filter(editors_choice=True, status='published')
    featured = BlogPost.objects.filter(featured=True, status='published')

    context = {
        'posts': posts,
        'spotlight': spotlight,
        'editors_choice': editors_choice,
        'featured': featured
    }

    return render(request, 'pages/home.html', context)



def blogs(request):

    category = request.GET.get('category', '')

    # Get filtered posts
    if category:
        posts = BlogPost.objects.filter(content_type=category, status='published').order_by('-created_at')
    else:
        posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    
    # Get total counts for display
    total_posts = BlogPost.objects.filter(status='published').count()
    total_filtered_posts = posts.count()
    
    # Pagination - 6 posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,  
        'total_posts': total_posts,
        'total_filtered_posts': total_filtered_posts,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,  # For pagination controls
        'selected_category': category,  # Pass selected category 
        'all_categories': BlogPost.CONTENT_TYPES, 
    }
    
    return render(request, 'pages/blogs.html', context)



def about(request):
    return render(request, 'pages/about.html')


@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        nm = request.POST.get('name')
        em = request.POST.get('email')
        pnum = request.POST.get('pnumber')
        msg = request.POST.get('message')

        if nm and em and msg:
            try:
                user = Contact(name=nm, email=em, pnumber=pnum, message=msg)
                user.save()
                return render(request, "pages/contact.html", {'success': True})
            except Exception as e:
                print(f"Error: {e}")
                return render(request, "pages/contact.html", {'error': True})
        else:
            return render(request, "pages/contact.html", {'error': True})
    
    return render(request, "pages/contact.html")


@login_required(login_url='login')
def blog_detail(request, id):
    blog = get_object_or_404(BlogPost, pk=id)
    
    # Increment views
    blog.increment_views()
    
    # Get approved comments 
    comments = blog.comments.filter(is_approved=True).order_by('-created_at')[:5]
    total_comments = blog.comments.filter(is_approved=True).count()
    
    # Handle POST requests
    if request.method == 'POST':
        # Handle like/dislike
        if 'like' in request.POST:
            blog.add_like()
            messages.success(request, 'Thanks for your like!')
            return redirect('blog_detail', id=id)
        
        elif 'dislike' in request.POST:
            blog.add_dislike()
            messages.success(request, 'Thanks for your feedback!')
            return redirect('blog_detail', id=id)
        
        # Handle comment submission
        else:
            author_name = request.POST.get('author_name', '').strip()
            author_email = request.POST.get('author_email', '').strip()
            comment_text = request.POST.get('comment_text', '').strip()
            
            # Validate required fields
            if author_name and comment_text:
                try:
                    # Create comment
                    comment = Comment.objects.create(
                        blog_post=blog,
                        author_name=author_name,
                        author_email=author_email if author_email else '',
                        comment_text=comment_text,
                        is_approved=False 
                    )
                    comment.save()
                    messages.success(request, 'Your comment has been submitted!')
                    return redirect('blog_detail', id=id)
                except Exception as e:
                    print(f"Error: {e}")
                    return redirect('blog_detail', id=id)
            else:
                messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'blog': blog,
        'comments': comments,
        'total_comments': total_comments,
    }
    
    return render(request, 'pages/blog_detail.html', context)



def search_results(request):
    query = request.GET.get('q', '').strip()
    results = BlogPost.objects.filter(status='published') 
    
    if query:
        # Search in title OR author fields (username, first_name, last_name)
        results = results.filter(
            Q(title__icontains=query) | 
            Q(author__username__icontains=query) |  # Search in username
            Q(author__first_name__icontains=query) |  # Search in first name
            Q(author__last_name__icontains=query)  # Search in last name
        ).distinct().order_by('-created_at')  # distinct() prevents duplicates
    
    # Pagination - 12 results per page
    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'results': page_obj,
    }
    
    return render(request, 'pages/search_results.html', context)




# Auth views
def login_view(request):
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Basic validation
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'auth/login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Redirect to next page if provided, otherwise home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password')
            return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')



def signup_view(request):
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2') 
        phone_number = request.POST.get('phone_number', '')
        bio = request.POST.get('bio', '')
        
        # Validate required fields
        if not username or not email or not password1:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'auth/sign_up.html')
        
        # Check password confirmation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/sign_up.html')
        
        # Check if user exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/sign_up.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/sign_up.html')
        
        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone_number=phone_number,
                bio=bio
            )
            
            # Auto-login the user
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}! Your account has been created.')
                return redirect('login')  
            
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'auth/sign_up.html')
    
    return render(request, 'auth/sign_up.html')




# user views
@login_required
def profile_view(request):
    user = request.user
    # Get counts for each status
    published_count = BlogPost.objects.filter(author=user, status='published').count()
    draft_count = BlogPost.objects.filter(author=user, status='draft').count()
    archived_count = BlogPost.objects.filter(author=user, status='archived').count()
    
    # Get total likes from published posts only
    total_likes = BlogPost.objects.filter(author=user, status='published').aggregate(
        total_likes=Sum('likes') 
    )['total_likes'] or 0 # Handle case where user has no published posts
    
    context = {
        'user': user,
        'published_count': published_count,
        'draft_count': draft_count,
        'archived_count': archived_count,
        'total_likes': total_likes,
    }
    
    return render(request, 'user/profile.html', context)



@login_required
def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('username', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            bio = request.POST.get('bio', '').strip()
            profile_picture = request.FILES.get('profile_picture')
            
            # Validate required fields
            if not username:
                messages.error(request, 'Username is required.')
                return render(request, 'user/edit_profile.html', {'user': user})
            
            if not email:
                messages.error(request, 'Email is required.')
                return render(request, 'user/edit_profile.html', {'user': user})
            
            # Check if username is taken (excluding current user)
            if CustomUser.objects.exclude(pk=user.pk).filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return render(request, 'user/edit_profile.html', {'user': user})
            
            # Check if email is taken (excluding current user)
            if CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'user/edit_profile.html', {'user': user})
            
            # Update user fields
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.bio = bio
            
            # Update profile picture if new one provided
            if profile_picture:
                # Validate image size (5MB max)
                if profile_picture.size > 5 * 1024 * 1024:
                    messages.error(request, 'Profile picture size should be less than 5MB.')
                    return render(request, 'user/edit_profile.html', {'user': user})
                
                # Validate image type
                valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if profile_picture.content_type not in valid_types:
                    messages.error(request, 'Invalid image format. Please upload JPG, PNG, GIF, or WebP.')
                    return render(request, 'user/edit_profile.html', {'user': user})
                
                # Delete old profile picture if it exists
                if user.profile_picture:
                    user.profile_picture.delete(save=False)
                
                user.profile_picture = profile_picture
            
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'user/edit_profile.html', {'user': user})
    
    return render(request, 'user/edit_profile.html', {'user': user})




# Blog views
@login_required
def write_blog_view(request):

    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title', '').strip()
            content = request.POST.get('content', '').strip()
            content_type = request.POST.get('content_type', '')
            image = request.FILES.get('image')
            action = request.POST.get('action', 'publish')
            
            # Validate required fields
            if not title:
                messages.error(request, 'Blog title is required.')
                return render(request, 'blog/write_blog.html')
            
            if not content:
                messages.error(request, 'Blog content is required.')
                return render(request, 'blog/write_blog.html')
            
            if not content_type:
                messages.error(request, 'Please select a category.')
                return render(request, 'blog/write_blog.html')
            
            if not image:
                messages.error(request, 'Featured image is required.')
                return render(request, 'blog/write_blog.html')
            
            # Validate content type choice
            valid_content_types = dict(BlogPost.CONTENT_TYPES).keys()
            if content_type not in valid_content_types:
                messages.error(request, 'Invalid category selected.')
                return render(request, 'blog/write_blog.html')
            
            # Create blog post
            blog_post = BlogPost(
                title=title,
                content=content,
                content_type=content_type,
                author=request.user,
                image=image,
            )
            
            # Set status based on action
            if action == 'draft':
                blog_post.status = 'draft'
                messages.success(request, 'Blog saved as draft successfully!')
                redirect = 'my_drafts'  # Redirect to drafts page
            else:  # publish
                blog_post.status = 'published'
                messages.success(request, 'Blog published successfully!')
                redirect = 'profile'  # Redirect to blog detail
            
            # Save the blog post
            blog_post.save()
            
            # Redirect based on action
            if action == 'draft':
                return redirect('my_drafts')  # Redirect to drafts page
            else:
                return redirect('blog_detail', pk=blog_post.pk)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'blog/write_blog.html')
        
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating blog post: {str(e)}")
            return render(request, 'blog/write_blog.html')
    
    # GET request - show empty form
    return render(request, 'blog/write_blog.html')



@login_required
def preview_blog_view(request, id):
    blog = get_object_or_404(BlogPost, pk=id)
    
    # Check if user is the author or staff
    if not request.user.is_staff and blog.author != request.user:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')
    
    # Handle POST request for publishing
    if request.method == 'POST':
        if 'publish' in request.POST:
            # Publish the blog
            blog.status = 'published'
            blog.save()
            messages.success(request, '✅ Blog published successfully! It is now live.')
            
            # Redirect to blog detail page or profile
            return redirect('blog_detail', id=blog.pk)
        
        elif 'archive' in request.POST:
            # Archive the blog
            blog.status = 'archived'
            blog.save()
            messages.success(request, '📦 Blog archived successfully.')
            return redirect('profile')
    
    # Get reading time
    word_count = len(blog.content.split())
    reading_time = max(1, word_count // 200)  # Assuming 200 words per minute reading speed
    
    context = {
        'blog': blog,
        'reading_time': reading_time,
        'word_count': word_count,
    }
    
    return render(request, 'blog/preview_blog.html', context)



@login_required
def edit_blog_view(request, id):
    blog_post = get_object_or_404(BlogPost, pk=id, author=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data from hidden inputs
            title = request.POST.get('title', '').strip()
            content = request.POST.get('content', '').strip()
            content_type = request.POST.get('content_type', '')
            keep_image = request.POST.get('keep_image') == 'on'
            new_image = request.FILES.get('new_image')
            
            # Validate required fields
            if not title:
                messages.error(request, 'Blog title is required.')
                return render(request, 'blog/edit_blog.html', {'blog': blog_post})
            
            if not content:
                messages.error(request, 'Blog content is required.')
                return render(request, 'blog/edit_blog.html', {'blog': blog_post})
            
            if not content_type:
                messages.error(request, 'Please select a category.')
                return render(request, 'blog/edit_blog.html', {'blog': blog_post})
            
            # Update blog post
            blog_post.title = title
            blog_post.content = content
            blog_post.content_type = content_type
            
            # Handle image
            if new_image and not keep_image:
                # Validate image size
                if new_image.size > 5 * 1024 * 1024:
                    messages.error(request, 'Image size should be less than 5MB.')
                    return render(request, 'blog/edit_blog.html', {'blog': blog_post})
                
                # Delete old image if it exists
                if blog_post.image:
                    blog_post.image.delete(save=False)
                
                blog_post.image = new_image
            
            blog_post.save()
            
            messages.success(request, f'Blog "{blog_post.title}" has been updated successfully!')
            return redirect('preview_blog', id=blog_post.id)
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'blog/edit_blog.html', {'blog': blog_post})
    
    return render(request, 'blog/edit_blog.html', {'blog': blog_post})




# Other blog management views
@login_required
def archive_blog_view(request, id):

    if request.method == 'POST':
        blog = get_object_or_404(BlogPost, id=id, author=request.user)
        blog_title = blog.title
        blog.status = 'archived'
        blog.save()
        messages.success(request, f'Blog "{blog_title}" has been archived successfully.')
        return redirect('profile')
    
    return redirect('profile')




@login_required
def publish_blog_view(request, id):

    if request.method == 'POST':
        blog = get_object_or_404(BlogPost, id=id, author=request.user)
        old_status = blog.status
        blog.status = 'published'
        blog.save()
        
        if old_status == 'archived':
            messages.success(request, f'Blog "{blog.title}" has been republished successfully!')
        else:
            messages.success(request, f'Blog "{blog.title}" has been published successfully!')
            
        return redirect('blog_detail', id=blog.pk)
    
    return redirect('profile')




@login_required
def delete_blog_view(request, id):

    if request.method == 'POST':
        blog = get_object_or_404(BlogPost, id=id, author=request.user)
        blog_title = blog.title
        blog.delete()
        messages.success(request, f'Blog "{blog_title}" has been deleted successfully.')
        return redirect('profile')
    
    return redirect('profile')