
echo "🚀 Starting build process..."
set -o errexit

echo "🐍 Python version:"
python --version

echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing requirements..."
python -m pip install -r requirements.txt

echo "📦 Installed packages:"
pip list

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running migrations..."
python manage.py migrate

echo "📝 Creating dummy blogs..."
python manage.py add_dummy_blogs --noinput



# ===== Auto-attach images to blogs =====
echo "📸 Auto-attaching images to blogs..."
python -c "
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogs.settings')
django.setup()

from app.models import BlogPost
from django.core.files import File
from django.conf import settings

def attach_images():
    print('🔍 Looking for blogs without images...')
    
    blogs = BlogPost.objects.filter(image='')
    total = blogs.count()
    
    if total == 0:
        print('✅ All blogs already have images!')
        return
    
    print(f'📊 Found {total} blogs without images')
    
    # CORRECT PATH: Images are in app/static/dummy_blogs_images/
    images_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'dummy_blogs_images')
    print(f'📁 Looking for images in: {images_path}')
    
    if not os.path.exists(images_path):
        print(f'❌ Images folder not found at: {images_path}')
        # List what's in app/static for debugging
        app_static_path = os.path.join(settings.BASE_DIR, 'app', 'static')
        if os.path.exists(app_static_path):
            print(f'Contents of app/static/: {os.listdir(app_static_path)}')
        else:
            print('app/static folder missing!')
        return
    
    print(f'📁 Images folder found with {len(os.listdir(images_path))} files')
    print(f'Sample images: {os.listdir(images_path)[:5]}')
    
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
    
    attached = 0
    for blog in blogs:
        category = blog.content_type
        base_name = category_map.get(category, 'default')
        
        image_attached = False
        for i in range(1, 6):
            for ext in ['.jpg', '.jpeg', '.png']:
                image_filename = f'{base_name}-{i}{ext}'
                image_path = os.path.join(images_path, image_filename)
                
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as f:
                            new_filename = f'{category.lower()}_{blog.id}_{image_filename}'
                            blog.image.save(new_filename, File(f), save=True)
                            print(f'  ✅ Attached: {image_filename} to blog {blog.id}')
                            attached += 1
                            image_attached = True
                            break
                    except Exception as e:
                        print(f'  ❌ Error attaching {image_filename}: {e}')
            if image_attached:
                break
        
        if not image_attached:
            print(f'  ⚠️ No image found for {category} blog {blog.id} (tried {base_name}-1.jpg through {base_name}-5.jpg)')
    
    print(f'\n📋 SUMMARY: Attached images to {attached} out of {total} blogs')

attach_images()
"

echo "📋 Final check:"
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogs.settings')
django.setup()
from app.models import BlogPost
total = BlogPost.objects.count()
with_images = BlogPost.objects.exclude(image='').count()
print(f'   Total blogs: {total}')
print(f'   Blogs with images: {with_images}')
print(f'   Blogs without images: {total - with_images}')
"