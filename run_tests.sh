#!/bin/bash
# Quick test runner script

echo "🧪 Running all tests..."
echo ""

./venv/bin/pytest tests/test_collision_physics.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi
