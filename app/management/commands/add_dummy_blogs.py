# blog/management/commands/create_dummy_blogs.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from blog.models import BlogPost
from datetime import datetime, timedelta
import os
import random
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 45 dummy blog posts (5 per category) with local images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing dummy blogs before creating new ones'
        )
        parser.add_argument(
            '--author',
            type=str,
            default='Deepak',
            choices=['Deepak', 'Anmol', 'Kishor', 'Tushar', 'Samuel', 'Alex'],
            help='Author name for the blogs (default: Deepak)'
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Do not prompt for confirmation'
        )

    def handle(self, *args, **options):
        clear = options['clear']
        author_name = options['author']
        noinput = options['noinput']
        
        self.stdout.write(self.style.WARNING(f'\n🔧 Dummy Blog Creation Tool'))
        self.stdout.write(f'{"="*50}')
        self.stdout.write(f'Author: {author_name}')
        self.stdout.write(f'Total blogs: 45 (5 per category)')
        self.stdout.write(f'{"="*50}')
        
        if clear:
            self.stdout.write(self.style.WARNING('⚠️  You are about to DELETE all existing dummy blogs!'))
            if not noinput:
                confirm = input('Are you sure you want to continue? (yes/no): ')
                if confirm.lower() != 'yes':
                    self.stdout.write(self.style.SUCCESS('Operation cancelled.'))
                    return
            self.clear_dummy_blogs()
        
        self.create_dummy_blogs(author_name)
    
    def get_image_for_category(self, category, index):
        """
        Get a local image file based on category and index
        """
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
        
        # Get the base filename pattern
        base_name = category_map.get(category, 'default')
        
        # Try different possible filename patterns
        possible_patterns = [
            f'{base_name}-{index}.jpg',
            f'{base_name}-{index}.jpeg',
            f'{base_name}-{index}.png',
            f'{base_name}-1.jpg',  # Fallback to first image
        ]
        
        # Path to your blog_images folder
        images_path = os.path.join(settings.BASE_DIR, 'static', 'dummy_blogs_images')
        
        for pattern in possible_patterns:
            image_path = os.path.join(images_path, pattern)
            if os.path.exists(image_path):
                return image_path
        
        return None

    def create_dummy_blogs(self, author_name):
        self.stdout.write(self.style.SUCCESS('\n🚀 Starting dummy blog creation...'))
        
        # Create username from author name (lowercase)
        username = author_name.lower()
        
        # Get or create dummy user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': author_name,
                'last_name': 'Author',
            }
        )
        
        if created:
            user.set_password('dummypass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Created new user: {user.username}'))
        else:
            self.stdout.write(f'✅ Using existing user: {user.username}')
        
        # 5 blogs per category using your existing content
        dummy_blogs = [
            # ========== BUSINESS (5 blogs) ==========
            {
                'title': 'Future of Remote Work in 2024',
                'content': 'The evolution of remote work post-pandemic and what companies need to adapt.',
                'content_type': 'Business',
                'spotlight': True,
                'likes': 1240,
                'views': 5600,
                'dislikes': 45,
            },
            {
                'title': 'Startup Funding Strategies',
                'content': 'How to secure funding for your startup in today\'s competitive market.',
                'content_type': 'Business',
                'featured': True,
                'likes': 890,
                'views': 3200,
                'dislikes': 12,
            },
            {
                'title': 'Sustainable Business Practices',
                'content': 'Eco-friendly practices that actually improve your bottom line.',
                'content_type': 'Business',
                'likes': 1560,
                'views': 6100,
                'dislikes': 23,
            },
            {
                'title': 'Digital Marketing Trends',
                'content': 'Latest trends in digital marketing that you should implement now.',
                'content_type': 'Business',
                'editors_choice': True,
                'likes': 980,
                'views': 4100,
                'dislikes': 18,
            },
            {
                'title': 'Leadership in Crisis',
                'content': 'How to lead your team effectively during challenging times.',
                'content_type': 'Business',
                'likes': 720,
                'views': 2900,
                'dislikes': 9,
            },
            
            # ========== TRAVEL (5 blogs) ==========
            {
                'title': 'Hidden Gems of Thailand',
                'content': 'Lesser-known destinations in Thailand that will blow your mind.',
                'content_type': 'Travel',
                'spotlight': True,
                'likes': 1890,
                'views': 7200,
                'dislikes': 34,
            },
            {
                'title': 'Budget Travel Europe',
                'content': 'How to explore Europe without breaking the bank.',
                'content_type': 'Travel',
                'likes': 1450,
                'views': 6100,
                'dislikes': 28,
            },
            {
                'title': 'Solo Travel Safety Tips',
                'content': 'Essential safety tips for solo travelers around the world.',
                'content_type': 'Travel',
                'featured': True,
                'likes': 1320,
                'views': 5800,
                'dislikes': 15,
            },
            {
                'title': 'Sustainable Tourism',
                'content': 'How to travel responsibly and minimize your environmental impact.',
                'content_type': 'Travel',
                'likes': 1100,
                'views': 4900,
                'dislikes': 21,
            },
            {
                'title': 'Best Road Trips in USA',
                'content': 'Top 5 scenic road trips you must experience in the USA.',
                'content_type': 'Travel',
                'editors_choice': True,
                'likes': 1680,
                'views': 6900,
                'dislikes': 42,
            },
            
            # ========== SPORTS (5 blogs) ==========
            {
                'title': 'Mental Training for Athletes',
                'content': 'Psychological techniques to enhance athletic performance.',
                'content_type': 'Sports',
                'likes': 1780,
                'views': 6800,
                'dislikes': 56,
            },
            {
                'title': 'Home Workouts That Work',
                'content': 'Effective workout routines you can do without gym equipment.',
                'content_type': 'Sports',
                'featured': True,
                'likes': 2450,
                'views': 10200,
                'dislikes': 89,
            },
            {
                'title': 'Sports Nutrition Guide',
                'content': 'Optimal nutrition for different types of athletes.',
                'content_type': 'Sports',
                'likes': 1560,
                'views': 7200,
                'dislikes': 34,
            },
            {
                'title': 'Injury Prevention Strategies',
                'content': 'How to prevent common sports injuries.',
                'content_type': 'Sports',
                'likes': 1320,
                'views': 5900,
                'dislikes': 27,
            },
            {
                'title': 'Future of Esports',
                'content': 'The rapid growth and future prospects of competitive gaming.',
                'content_type': 'Sports',
                'spotlight': True,
                'likes': 1890,
                'views': 8100,
                'dislikes': 123,
            },
            
            # ========== FOOD (5 blogs) ==========
            {
                'title': 'Plant-Based Cooking Basics',
                'content': 'Getting started with delicious plant-based meals.',
                'content_type': 'Food',
                'likes': 1680,
                'views': 7100,
                'dislikes': 45,
            },
            {
                'title': 'Art of Fermentation',
                'content': 'Learn to make your own kimchi, sauerkraut, and kombucha.',
                'content_type': 'Food',
                'editors_choice': True,
                'likes': 1420,
                'views': 6300,
                'dislikes': 38,
            },
            {
                'title': 'Quick Weeknight Dinners',
                'content': '30-minute meals for busy weeknights.',
                'content_type': 'Food',
                'featured': True,
                'likes': 1980,
                'views': 8400,
                'dislikes': 67,
            },
            {
                'title': 'Baking Perfect Sourdough',
                'content': 'Step-by-step guide to mastering sourdough bread.',
                'content_type': 'Food',
                'likes': 1760,
                'views': 7500,
                'dislikes': 52,
            },
            {
                'title': 'Global Street Food Recipes',
                'content': 'Recreate popular street foods from around the world.',
                'content_type': 'Food',
                'likes': 1540,
                'views': 6900,
                'dislikes': 41,
            },
            
            # ========== FASHION (5 blogs) ==========
            {
                'title': 'Sustainable Fashion Brands',
                'content': 'Eco-friendly fashion labels worth supporting.',
                'content_type': 'Fashion',
                'likes': 1450,
                'views': 6200,
                'dislikes': 36,
            },
            {
                'title': 'Capsule Wardrobe Essentials',
                'content': 'Build a versatile wardrobe with fewer pieces.',
                'content_type': 'Fashion',
                'spotlight': True,
                'likes': 1670,
                'views': 7100,
                'dislikes': 48,
            },
            {
                'title': '90s Fashion Comeback',
                'content': 'How 90s trends are making a modern return.',
                'content_type': 'Fashion',
                'likes': 1280,
                'views': 5400,
                'dislikes': 32,
            },
            {
                'title': 'Work From Home Style',
                'content': 'Looking professional while working from home.',
                'content_type': 'Fashion',
                'editors_choice': True,
                'likes': 1120,
                'views': 4900,
                'dislikes': 24,
            },
            {
                'title': 'Investment Fashion Pieces',
                'content': 'High-quality items worth splurging on.',
                'content_type': 'Fashion',
                'likes': 1340,
                'views': 5700,
                'dislikes': 31,
            },
            
            # ========== TECHNOLOGY (5 blogs) ==========
            {
                'title': 'AI for Beginners',
                'content': 'Getting started with artificial intelligence programming.',
                'content_type': 'Technology',
                'featured': True,
                'likes': 2340,
                'views': 9800,
                'dislikes': 78,
            },
            {
                'title': 'Smart Home Security',
                'content': 'Protecting your connected home from digital threats.',
                'content_type': 'Technology',
                'likes': 1670,
                'views': 7200,
                'dislikes': 42,
            },
            {
                'title': 'Future of Electric Vehicles',
                'content': 'Latest advancements in EV technology.',
                'content_type': 'Technology',
                'likes': 1890,
                'views': 8100,
                'dislikes': 56,
            },
            {
                'title': 'Blockchain Beyond Crypto',
                'content': 'Practical applications of blockchain technology.',
                'content_type': 'Technology',
                'editors_choice': True,
                'likes': 1540,
                'views': 6800,
                'dislikes': 45,
            },
            {
                'title': 'Web Development Trends 2024',
                'content': 'Latest trends in web development and design.',
                'content_type': 'Technology',
                'spotlight': True,
                'likes': 1980,
                'views': 8600,
                'dislikes': 67,
            },
            
            # ========== CREATIVE (5 blogs) ==========
            {
                'title': 'Digital Art Techniques',
                'content': 'Essential techniques for digital painting and illustration.',
                'content_type': 'Creative',
                'likes': 1670,
                'views': 6900,
                'dislikes': 38,
            },
            {
                'title': 'Photography Composition Rules',
                'content': 'Fundamental rules for creating compelling photos.',
                'content_type': 'Creative',
                'likes': 1450,
                'views': 6300,
                'dislikes': 34,
            },
            {
                'title': 'Creative Writing Prompts',
                'content': '50 prompts to overcome writer\'s block.',
                'content_type': 'Creative',
                'featured': True,
                'likes': 1230,
                'views': 5400,
                'dislikes': 28,
            },
            {
                'title': 'DIY Home Decor Projects',
                'content': 'Easy and affordable home decor ideas.',
                'content_type': 'Creative',
                'likes': 1560,
                'views': 6700,
                'dislikes': 41,
            },
            {
                'title': 'Music Production Basics',
                'content': 'Getting started with digital music production.',
                'content_type': 'Creative',
                'likes': 1340,
                'views': 5800,
                'dislikes': 32,
            },
            
            # ========== HEALTH (5 blogs) ==========
            {
                'title': 'Gut Health Explained',
                'content': 'Understanding and improving your gut microbiome.',
                'content_type': 'Health',
                'likes': 1890,
                'views': 8200,
                'dislikes': 45,
            },
            {
                'title': 'Sleep Optimization',
                'content': 'Science-backed methods for better sleep.',
                'content_type': 'Health',
                'spotlight': True,
                'likes': 1760,
                'views': 7600,
                'dislikes': 52,
            },
            {
                'title': 'Mindfulness Meditation',
                'content': 'Beginner\'s guide to mindfulness practice.',
                'content_type': 'Health',
                'likes': 1670,
                'views': 7100,
                'dislikes': 48,
            },
            {
                'title': 'Nutrition Myths Debunked',
                'content': 'Common nutrition misconceptions explained.',
                'content_type': 'Health',
                'likes': 1540,
                'views': 6800,
                'dislikes': 42,
            },
            {
                'title': 'Building Exercise Habits',
                'content': 'How to make exercise a consistent part of your life.',
                'content_type': 'Health',
                'editors_choice': True,
                'likes': 1340,
                'views': 5900,
                'dislikes': 36,
            },
            
            # ========== ENTERTAINMENT (5 blogs) ==========
            {
                'title': 'Underrated Movies to Watch',
                'content': 'Hidden cinematic gems you might have missed.',
                'content_type': 'Entertainment',
                'likes': 1760,
                'views': 7400,
                'dislikes': 51,
            },
            {
                'title': 'True Crime Podcast Guide',
                'content': 'Best true crime podcasts for enthusiasts.',
                'content_type': 'Entertainment',
                'featured': True,
                'likes': 1450,
                'views': 6300,
                'dislikes': 42,
            },
            {
                'title': 'Video Games as Art',
                'content': 'Games that push the boundaries of storytelling.',
                'content_type': 'Entertainment',
                'likes': 1890,
                'views': 8100,
                'dislikes': 89,
            },
            {
                'title': 'Stand-Up Comedy Evolution',
                'content': 'How stand-up comedy has changed over decades.',
                'content_type': 'Entertainment',
                'likes': 1230,
                'views': 5400,
                'dislikes': 34,
            },
            {
                'title': 'Book Recommendations 2024',
                'content': 'Must-read books released this year.',
                'content_type': 'Entertainment',
                'editors_choice': True,
                'likes': 1560,
                'views': 6700,
                'dislikes': 45,
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        self.stdout.write('⏳ Creating blogs', ending='')
        
        # Track image index per category
        category_counters = {}
        
        for i, blog_data in enumerate(dummy_blogs):
            # Progress indicator
            if i % 5 == 0:
                self.stdout.write('.', ending='')
                self.stdout.flush()
            
            # Get category and increment counter
            category = blog_data['content_type']
            category_counters[category] = category_counters.get(category, 0) + 1
            image_index = category_counters[category]
            
            # Random creation date (within last 365 days)
            days_ago = random.randint(1, 365)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            # Create blog post
            blog, created = BlogPost.objects.get_or_create(
                title=blog_data['title'],
                defaults={
                    'content': blog_data['content'],
                    'content_type': category,
                    'author': user,
                    'created_at': created_at,
                    'spotlight': blog_data.get('spotlight', False),
                    'editors_choice': blog_data.get('editors_choice', False),
                    'featured': blog_data.get('featured', False),
                    'likes': blog_data['likes'],
                    'dislikes': blog_data['dislikes'],
                    'views': blog_data['views'],
                    'status': 'published',
                }
            )
            
            # Add image if blog was created
            if created:
                image_path = self.get_image_for_category(category, image_index)
                if image_path:
                    with open(image_path, 'rb') as f:
                        # Generate a unique filename for the blog
                        filename = f'{category.lower()}_{blog.id}_{os.path.basename(image_path)}'
                        blog.image.save(filename, File(f), save=True)
                created_count += 1
            else:
                existing_count += 1
        
        self.stdout.write('')  # New line after progress dots
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n{"="*50}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Creation Complete!'))
        self.stdout.write(f'   New blogs created: {created_count}')
        self.stdout.write(f'   Existing blogs: {existing_count}')
        self.stdout.write(f'   Total blogs now: {BlogPost.objects.filter(author=user).count()}')
        self.stdout.write(f'   Author: {user.first_name} {user.last_name} ({user.username})')
        self.stdout.write(f'   Categories: Business, Travel, Sports, Food, Fashion, Technology, Creative, Health, Entertainment')
        self.stdout.write(self.style.SUCCESS(f'{"="*50}'))
        
        # Show image mapping
        self.stdout.write(self.style.SUCCESS('\n📸 Image Mapping:'))
        for category, count in category_counters.items():
            self.stdout.write(f'   {category}: used {count} images')
    
    def clear_dummy_blogs(self):
        """Delete all blogs created by dummy authors"""
        authors = ['deepak', 'anmol', 'kishor', 'tushar', 'samuel', 'alex']
        total_deleted = 0
        
        for username in authors:
            try:
                user = User.objects.get(username=username)
                count, _ = BlogPost.objects.filter(author=user).delete()
                if count > 0:
                    self.stdout.write(self.style.SUCCESS(f'🗑️ Deleted {count} blogs by {username}'))
                    total_deleted += count
            except User.DoesNotExist:
                pass
        
        if total_deleted == 0:
            self.stdout.write(self.style.WARNING('⚠️ No dummy blogs found to delete'))
        else:
            self.stdout.write(self.style.SUCCESS(f'🗑️ Total deleted: {total_deleted} blogs'))