from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[

  # Page urls
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('search/', views.search_results, name='search_results'),

  # Auth urls
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign_up/', views.signup_view, name='signup'),

  # user urls
    path('profile/', views.profile_view, name='profile'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'), 

  # Blog urls  
    path('write/', views.write_blog_view, name='write_blog'),
    path('edit/<int:id>/', views.edit_blog_view, name='edit_blog'),

  # Other urls
    path('preview/<int:id>/', views.preview_blog_view, name='preview_blog'),
    path('archive/<int:id>/', views.archive_blog_view, name='archive_blog'),
    path('publish/<int:id>/', views.publish_blog_view, name='publish_blog'),
    path('delete/<int:id>/', views.delete_blog_view, name='delete_blog'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)