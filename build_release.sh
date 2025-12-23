#!/bin/bash
# Complete build process with obfuscation for Siena's Snowy Adventure
# This script orchestrates the entire release build pipeline

set -e  # Exit on any error

VERSION=$(cat VERSION | tr -d '\n')

echo "======================================"
echo "Siena's Snowy Adventure Build Pipeline"
echo "Version: $VERSION"
echo "======================================"
echo ""

# Step 1: Obfuscate source code
echo "🔒 Step 1: Obfuscating source code..."
./build_obfuscated.sh
if [ $? -ne 0 ]; then
    echo "❌ Obfuscation failed!"
    exit 1
fi
echo "✅ Obfuscation complete"
echo ""

# Step 2: Build with PyInstaller
echo "📦 Step 2: Building with PyInstaller..."
./venv/bin/pyinstaller siena_snowy_adventure_obfuscated.spec --clean
if [ $? -ne 0 ]; then
    echo "❌ PyInstaller build failed!"
    exit 1
fi
echo "✅ Build complete"
echo ""

# Step 3: Create distribution ZIP
echo "🗜️ Step 3: Creating distribution ZIP..."
cd dist
if [ -f "SienaSnowyAdventure-Mac-v${VERSION}.zip" ]; then
    echo "  Removing existing ZIP..."
    rm "SienaSnowyAdventure-Mac-v${VERSION}.zip"
fi
zip -r -q "SienaSnowyAdventure-Mac-v${VERSION}.zip" SienaSnowyAdventure.app
if [ $? -ne 0 ]; then
    echo "❌ ZIP creation failed!"
    cd ..
    exit 1
fi
cd ..
echo "✅ ZIP created"
echo ""

# Step 4: Calculate file size
FILE_SIZE=$(du -h "dist/SienaSnowyAdventure-Mac-v${VERSION}.zip" | cut -f1)

echo "======================================"
echo "✅ BUILD COMPLETE!"
echo "======================================"
echo "📦 Distribution file: dist/SienaSnowyAdventure-Mac-v${VERSION}.zip"
echo "📏 File size: ${FILE_SIZE}"
echo ""
echo "Next steps:"
echo "1. Test the build: open dist/SienaSnowyAdventure.app"
echo "2. Create GitHub Release with tag v${VERSION}"
echo "3. Upload dist/SienaSnowyAdventure-Mac-v${VERSION}.zip to release"
echo "4. Update Firebase /version node with download URL"
echo ""
