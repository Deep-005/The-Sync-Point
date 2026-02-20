#!/usr/bin/env bash
# build.sh

echo "🚀 Starting build process..."

# Exit on error
set -o errexit

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install setuptools and wheel (these versions match your requirements)
echo "📦 Installing setuptools and wheel..."
python -m pip install setuptools==82.0.0 wheel==0.46.3

# Install requirements
echo "📦 Installing requirements..."
python -m pip install -r requirements.txt

# Verify pkg_resources is available
echo "🔍 Verifying pkg_resources..."
python -c "import pkg_resources; print('✅ pkg_resources found!')"

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Create dummy blogs
echo "📝 Creating dummy blogs..."
python manage.py add_dummy_blogs --noinput

echo "✅ Build complete!"