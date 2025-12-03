.PHONY: test test-verbose run help

help:
	@echo "Available commands:"
	@echo "  make test         - Run all tests"
	@echo "  make test-verbose - Run tests with detailed output"
	@echo "  make run          - Run the game"
	@echo "  make help         - Show this help message"

test:
	@echo "🧪 Running tests..."
	@./venv/bin/pytest tests/test_collision_physics.py -v

test-verbose:
	@echo "🧪 Running tests with verbose output..."
	@./venv/bin/pytest tests/test_collision_physics.py -vv --tb=short

run:
	@echo "🎮 Starting game..."
	@./venv/bin/python main.py
