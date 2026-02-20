#!/usr/bin/env bash
# build.sh

echo "🚀 Starting build process..."

# Exit on error
set -o errexit

# Show current Python version
echo "🐍 Python version:"
python --version

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# STEP 2: Now install the rest of requirements
echo "📦 Installing remaining requirements..."
python -m pip install -r requirements.txt

# Show installed packages
echo "📦 Installed packages:"
pip list

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Create dummy blogs
echo "📝 Creating dummy blogs..."
python manage.py add_dummy_blogs --noinput

# After creating dummy blogs
echo "📸 Attaching images to blogs..."
python attach_images.py

echo "✅ Build complete!"