# attach_images.py
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogs.settings')
django.setup()

from app.models import BlogPost
from django.core.files import File
from django.conf import settings

def attach_images_to_blogs():
    """Attach images from static/dummy_blog_images/ to blog posts"""
    
    print("🔍 Scanning for blogs without images...")
    
    # Get blogs without images
    blogs = BlogPost.objects.filter(image='')
    
    if not blogs.exists():
        # Try alternative filter
        blogs = BlogPost.objects.all()
        blogs_without_images = []
        for blog in blogs:
            if not blog.image or not blog.image.name:
                blogs_without_images.append(blog.id)
        blogs = BlogPost.objects.filter(id__in=blogs_without_images)
    
    total = blogs.count()
    print(f"📊 Found {total} blogs without images")
    
    if total == 0:
        print("✨ All blogs already have images!")
        return
    
    # CORRECT PATH: Your images are in static/dummy_blog_images/
    images_path = os.path.join(settings.BASE_DIR, 'static', 'dummy_blogs_images')
    print(f"📁 Looking for images in: {images_path}")
    
    if not os.path.exists(images_path):
        print(f"❌ ERROR: Images folder not found at {images_path}")
        print("Please make sure your images are in static/dummy_blogs_images/")
        return
    
    # Map categories to filename patterns
    category_map = {
        'Business': 'business',
        'Travel': 'travel',
        'Sports': 'sports',
        'Food': 'food',
        'Fashion': 'fashion',
        'Technology': 'tech',
        'Creative': 'creative',
        'Health': 'health',
        'Entertainment': 'ent',
    }
    
    success_count = 0
    failed_count = 0
    
    for blog in blogs:
        category = blog.content_type
        base_name = category_map.get(category, 'default')
        
        print(f"\n🔄 Processing: {blog.title} (ID: {blog.id}, Category: {category})")
        
        image_attached = False
        for i in range(1, 6):
            # Try different extensions
            for ext in ['.jpg', '.jpeg', '.png']:
                image_filename = f"{base_name}-{i}{ext}"
                image_path = os.path.join(images_path, image_filename)
                
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as f:
                            new_filename = f"{category.lower()}_{blog.id}_{image_filename}"
                            blog.image.save(new_filename, File(f), save=True)
                            print(f"  ✅ Attached: {image_filename}")
                            image_attached = True
                            success_count += 1
                            break
                    except Exception as e:
                        print(f"  ❌ Error attaching {image_filename}: {e}")
                        failed_count += 1
            
            if image_attached:
                break
        
        if not image_attached:
            print(f"  ⚠️ No image found for {category} (tried {base_name}-1.jpg through {base_name}-5.jpg)")
            failed_count += 1
    
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    print(f"✅ Successfully attached images: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total processed: {total}")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Starting image attachment script...")
    attach_images_to_blogs()