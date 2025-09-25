# Makefile for Agentic Chat Educational Content Generator

.PHONY: setup check docs clean install test lint format transcripts help

# Default target
help:
	@echo "Available targets:"
	@echo "  setup       - Set up virtual environment and install dependencies"
	@echo "  install     - Install package in development mode"
	@echo "  check       - Run quality checks on generated content"
	@echo "  docs        - Validate documentation and diagrams"
	@echo "  transcripts - Download video transcripts"
	@echo "  lint        - Run code linting (requires ruff)"
	@echo "  format      - Format code (requires black)"
	@echo "  test        - Run tests (when implemented)"
	@echo "  clean       - Clean temporary files and caches"

# Environment setup
setup:
	@echo "🔧 Setting up development environment..."
	uv venv
	@echo "🔧 Virtual environment created. Activate with:"
	@echo "   source .venv/bin/activate  # Linux/Mac"
	@echo "   .venv\\Scripts\\activate     # Windows"

install:
	@echo "📦 Installing package in development mode..."
	uv pip install -e .

transcripts:
	@echo "📺 Downloading video transcripts..."
	python scripts/download_transcripts.py

# Quality checks
check:
	@echo "🔍 Running content quality checks..."
	@python -c "import glob; [print(f'{f}: {sum(1 for _ in open(f, encoding=\"utf-8\", errors=\"ignore\"))} lines') for f in glob.glob('outputs/documents/*.md')]"
	@echo "📊 Generated content statistics:"
	@ls -lh outputs/ 2>/dev/null || echo "No outputs/ directory found"
	@ls -lh outputs/documents/ 2>/dev/null || echo "No outputs/documents/ directory found"
	@ls -lh outputs/diagrams/ 2>/dev/null || echo "No outputs/diagrams/ directory found"

docs:
	@echo "📚 Validating documentation..."
	@echo "Checking for required files:"
	@test -f README.md && echo "✅ README.md" || echo "❌ README.md missing"
	@test -f LICENSE && echo "✅ LICENSE" || echo "❌ LICENSE missing"
	@test -f pyproject.toml && echo "✅ pyproject.toml" || echo "❌ pyproject.toml missing"
	@test -d outputs/ && echo "✅ outputs/ directory" || echo "❌ outputs/ directory missing"
	@test -d outputs/documents/ && echo "✅ outputs/documents/ directory" || echo "❌ outputs/documents/ directory missing"
	@test -d outputs/diagrams/ && echo "✅ outputs/diagrams/ directory" || echo "❌ outputs/diagrams/ directory missing"

# Code quality (optional - requires tools)
lint:
	@echo "🧹 Running code linting..."
	@command -v ruff >/dev/null 2>&1 && ruff check . || echo "ruff not installed. Install with: pip install ruff"

format:
	@echo "🎨 Formatting code..."
	@command -v black >/dev/null 2>&1 && black . || echo "black not installed. Install with: pip install black"

# Testing (placeholder)
test:
	@echo "🧪 Running tests..."
	@echo "Tests not yet implemented. See CONTRIBUTING.md for testing guidelines."

# Cleanup
clean:
	@echo "🧽 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# CI target
ci: docs check
	@echo "🚀 CI checks complete"