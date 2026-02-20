
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

print('='*50)
print('DEBUGGING INFORMATION')
print('='*50)

print(f'Current directory: {os.getcwd()}')
print(f'Python path: {sys.path}')

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogs.settings')
django.setup()
print('✅ Django setup complete')

# Check if we can import the model
try:
    from app.models import BlogPost
    print('✅ Successfully imported BlogPost from app.models')
except Exception as e:
    print(f'❌ Failed to import BlogPost: {e}')

from django.core.files import File
from django.conf import settings

print(f'BASE_DIR: {settings.BASE_DIR}')

# Check static folder
static_path = os.path.join(settings.BASE_DIR, 'static')
print(f'Static path: {static_path}')
print(f'Static exists? {os.path.exists(static_path)}')

if os.path.exists(static_path):
    print(f'Static contents: {os.listdir(static_path)}')
    
    # Check images folder
    images_path = os.path.join(static_path, 'dummy_blogs_images')
    print(f'Images path: {images_path}')
    print(f'Images exists? {os.path.exists(images_path)}')
    
    if os.path.exists(images_path):
        print(f'Images found: {os.listdir(images_path)[:10]}')
    else:
        print('❌ Images folder not found!')
        
        # Try to find it anywhere
        print('Searching for dummy_blogs_images folder...')
        for root, dirs, files in os.walk(settings.BASE_DIR):
            if 'dummy_blogs_images' in dirs:
                print(f'Found at: {os.path.join(root, dummy_blogs_images)}')
else:
    print('❌ Static folder not found!')
    # Try to find static folder
    for root, dirs, files in os.walk(settings.BASE_DIR):
        if 'static' in dirs:
            print(f'Found static at: {os.path.join(root, static)}')

# Now try to attach images
try:
    from app.models import BlogPost
    
    def attach_images():
        print('\n🔍 Looking for blogs without images...')
        
        blogs = BlogPost.objects.filter(image='')
        total = blogs.count()
        print(f'📊 Found {total} blogs without images')
        
        if total == 0:
            print('✅ All blogs already have images!')
            return
        
        images_path = os.path.join(settings.BASE_DIR, 'static', 'dummy_blogs_images')
        
        if not os.path.exists(images_path):
            print(f'❌ Images folder not found at: {images_path}')
            return
        
        print(f'📁 Images folder found with {len(os.listdir(images_path))} files')
        
        category_map = {
            'Business': 'business', 'Travel': 'travel', 'Sports': 'sports',
            'Food': 'food', 'Fashion': 'fashion', 'Technology': 'tech',
            'Creative': 'creative', 'Health': 'health', 'Entertainment': 'ent',
        }
        
        attached = 0
        for blog in blogs:
            category = blog.content_type
            base_name = category_map.get(category, 'default')
            
            for i in range(1, 6):
                for ext in ['.jpg', '.jpeg', '.png']:
                    image_filename = f'{base_name}-{i}{ext}'
                    image_path = os.path.join(images_path, image_filename)
                    
                    if os.path.exists(image_path):
                        try:
                            with open(image_path, 'rb') as f:
                                new_filename = f'{category.lower()}_{blog.id}_{image_filename}'
                                blog.image.save(new_filename, File(f), save=True)
                                print(f'  ✅ Attached to blog {blog.id}')
                                attached += 1
                                break
                        except Exception as e:
                            print(f'  ❌ Error: {e}')
                    if blog.image:
                        break
            
            if not blog.image:
                print(f'  ⚠️ No image for {category} blog {blog.id}')
        
        print(f'\n📋 Attached images to {attached} blogs')
    
    attach_images()
    
except Exception as e:
    print(f'❌ Error in attachment process: {e}')
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