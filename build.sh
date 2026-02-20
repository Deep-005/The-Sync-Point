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

# STEP 1: Install setuptools and wheel FIRST (CRITICAL!)
echo "📦 Installing setuptools and wheel FIRST..."
python -m pip install --force-reinstall setuptools==82.0.0 wheel==0.46.3

# Verify pkg_resources is available NOW
echo "🔍 Verifying pkg_resources..."
python -c "import pkg_resources; print('✅ pkg_resources found after setuptools install!')"

# STEP 2: Now install the rest of requirements
echo "📦 Installing remaining requirements..."
python -m pip install -r requirements.txt

# Verify pkg_resources again
echo "🔍 Verifying pkg_resources still available..."
python -c "import pkg_resources; print('✅ pkg_resources still found!')"

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
python manage.py create_dummy_blogs --noinput

echo "✅ Build complete!"