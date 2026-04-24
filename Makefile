# To use this Makefile, ensure you have uv installed

# Configuration
SRC := protograf
PYTHON := 3.13

# Detect Operating System
ifeq ($(OS),Windows_NT)
    # Windows commands
    RM = rmdir /s /q
    MKDIR = mkdir
    BIN_PATH = .venv/Scripts
    PYTHON = $(BIN_PATH)/python.exe
    CD = chdir
    ZIPEX = tar -a -c --exclude="temp" -f examples.zip examples
    SAMPEX = ./all.bat
else
    # Linux/macOS commands
    RM = rm -rf
    MKDIR = mkdir -p
    BIN_PATH = .venv/bin
    PYTHON = $(BIN_PATH)/python
    CD = cd
    ZIPEX = zip -r examples.zip examples -x "temp/*"
    SAMPEX = ./all.sh
endif

.PHONY: help setup install format lint test docs examplez samples delete

# Show this help message
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Create the virtual environment using uv
setup:
	@echo "Creating virtual environment using uv..."
	uv venv --python $(PYTHON)

# Install dependencies using uv
install:
	@echo "Installing dependencies..."
	uv pip install -r requirements.txt

# Format code using Black
format:
	@echo "Formatting code with Black"
	uv run black --target-version py313 $(SRC)

# Run Black in check mode
lint:
	@echo "Checking code formatting with Black and pyrefly"
	uv run black --target-version py313 --check $(SRC)
	# uv run pyrefly $(SRC)

# Run tests using pytest
test:
	@echo "Running tests"
	uv run pytest --verbose

# Build documentation
docs:
	@echo "Building HTML docs"
	$(CD) docs
	uv run make html

# Create ZIPPED examples
examplez:
	@echo "Creating ZIP file with all examples"
	$(ZIPEX)

# Run built-in examples
samples:
	@echo "Running all built-in examples"
	$(CD) examples
	$(SAMPEX)

# Remove virtual environment and temporary files
delete:
	@echo "Cleaning up virtual environment"
	$(RM) .venv .pytest_cache .mypy_cache
	$(RM) __pycache__
