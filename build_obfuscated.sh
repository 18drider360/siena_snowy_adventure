#!/bin/bash
# Obfuscate Python source files with PyArmor
# Note: PyArmor trial has size limits, so we'll obfuscate selectively

echo "🔒 Starting code obfuscation..."

# Clean previous obfuscation
if [ -d "dist_obfuscated" ]; then
    echo "  Cleaning previous obfuscation..."
    rm -rf dist_obfuscated/
fi

# Create output directory structure
mkdir -p dist_obfuscated/src

# Obfuscate main entry point
echo "  Obfuscating main.py..."
./venv/bin/pyarmor gen --output dist_obfuscated main.py

# Obfuscate individual directories (avoiding large files)
echo "  Obfuscating src/core/..."
./venv/bin/pyarmor gen --output dist_obfuscated/src_temp/core --recursive src/core/
# Fix nested structure created by PyArmor
mv dist_obfuscated/src_temp/core/core/* dist_obfuscated/src_temp/core/ 2>/dev/null || true
mv dist_obfuscated/src_temp/core/pyarmor_runtime_000000 dist_obfuscated/
rm -rf dist_obfuscated/src_temp/core/core
mv dist_obfuscated/src_temp/core dist_obfuscated/src/

echo "  Obfuscating src/ui/..."
./venv/bin/pyarmor gen --output dist_obfuscated/src_temp/ui --recursive src/ui/
mv dist_obfuscated/src_temp/ui/ui/* dist_obfuscated/src_temp/ui/ 2>/dev/null || true
rm -rf dist_obfuscated/src_temp/ui/ui dist_obfuscated/src_temp/ui/pyarmor_runtime_000000
mv dist_obfuscated/src_temp/ui dist_obfuscated/src/

echo "  Obfuscating src/utils/..."
./venv/bin/pyarmor gen --output dist_obfuscated/src_temp/utils --recursive src/utils/
mv dist_obfuscated/src_temp/utils/utils/* dist_obfuscated/src_temp/utils/ 2>/dev/null || true
rm -rf dist_obfuscated/src_temp/utils/utils dist_obfuscated/src_temp/utils/pyarmor_runtime_000000
mv dist_obfuscated/src_temp/utils dist_obfuscated/src/

# Clean up temp directory
rm -rf dist_obfuscated/src_temp

# Copy src/data directory (story data)
echo "  Copying src/data/..."
mkdir -p dist_obfuscated/src/data
cp -r src/data/*.py dist_obfuscated/src/data/

# Copy src/levels directory (level definitions)
echo "  Copying src/levels/..."
mkdir -p dist_obfuscated/src/levels
cp -r src/levels/*.py dist_obfuscated/src/levels/

# Copy src/entities directory (player and enemies)
echo "  Copying src/entities/..."
mkdir -p dist_obfuscated/src/entities
cp -r src/entities dist_obfuscated/src/

# Copy large files without obfuscation (PyArmor trial limit workaround)
echo "  Copying src/rendering/ (files too large for trial license)..."
mkdir -p dist_obfuscated/src/rendering
mkdir -p dist_obfuscated/src/rendering/screens
cp -r src/rendering/*.py dist_obfuscated/src/rendering/
cp -r src/rendering/screens/*.py dist_obfuscated/src/rendering/screens/

# Copy src/__init__.py files
echo "  Copying __init__.py files..."
cp src/__init__.py dist_obfuscated/src/
cp src/data/__init__.py dist_obfuscated/src/data/
cp src/levels/__init__.py dist_obfuscated/src/levels/
cp src/rendering/__init__.py dist_obfuscated/src/rendering/
cp src/rendering/screens/__init__.py dist_obfuscated/src/rendering/screens/

# Copy non-Python files that are needed
echo "  Copying assets and configuration..."
cp -r assets dist_obfuscated/
cp config.yaml dist_obfuscated/
cp VERSION dist_obfuscated/
cp .env.example dist_obfuscated/

# Copy update installer script (needed for auto-updates)
if [ -f "update_installer.py" ]; then
    echo "  Copying update_installer.py..."
    cp update_installer.py dist_obfuscated/
fi

echo "✅ Obfuscation complete!"
echo "📁 Obfuscated code location: dist_obfuscated/"
echo "ℹ️  Note: src/rendering/* copied without obfuscation (PyArmor trial size limit)"
echo ""
echo "Next steps:"
echo "1. Review obfuscated files in dist_obfuscated/"
echo "2. Build with PyInstaller using obfuscated source"
echo "3. Test the obfuscated build"
