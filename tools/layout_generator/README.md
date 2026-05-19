# vibe

## 🔧 Development & Quality Control
To maintain a 10/10 score and pass strict static analysis:

```sh
# Ty checking
uv run --with ty ty check src

# Type checking
uv run --with mypy mypy src

# Fast linting
uv run --with ruff ruff check src

# Deep linting
uv run --with pylint pylint src

# Format code (--check to prevent autofix)
uv run --with black black src
```