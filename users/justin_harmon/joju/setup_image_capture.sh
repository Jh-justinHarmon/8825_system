#!/bin/bash

# Joju Image Capture System - Setup Script

echo "🎨 Setting up Joju Image Capture System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements_images.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Python dependencies installed"
echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright browsers"
    exit 1
fi

echo "✅ Playwright browsers installed"
echo ""

# Create content/media directory
echo "📁 Creating content/media directory..."
mkdir -p content/media

echo "✅ Directory structure created"
echo ""

# Make the Python script executable
chmod +x joju_image_capture.py

echo "✅ Made joju_image_capture.py executable"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your Figma token: https://www.figma.com/settings"
echo "2. Run: python3 joju_image_capture.py --config output/joju_upload_ready.json --figma-token YOUR_TOKEN"
echo ""
echo "See IMAGE_CAPTURE_README.md for full documentation"
