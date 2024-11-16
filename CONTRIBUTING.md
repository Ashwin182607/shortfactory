# Contributing to ShortFactory 🎬

Thank you for your interest in contributing to ShortFactory! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

1. Report bugs and issues
2. Suggest new features
3. Improve documentation
4. Submit code changes
5. Share example videos and templates

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/shortfactory.git
   cd shortfactory
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and modular

### Testing
1. Write tests for new features:
   ```bash
   pytest tests/
   ```
2. Ensure all tests pass before submitting
3. Maintain or improve code coverage

### Documentation
- Update relevant documentation
- Add docstrings to new functions
- Include example usage where appropriate
- Keep README.md up to date

## 🔄 Pull Request Process

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   # or
   git checkout -b fix/your-fix
   ```

2. Make your changes:
   - Write clear commit messages
   - Keep commits focused and atomic
   - Reference issues if applicable

3. Update documentation:
   - Add/update docstrings
   - Update README if needed
   - Add to CHANGELOG.md

4. Run tests and checks:
   ```bash
   # Run tests
   pytest

   # Check code style
   black .
   isort .
   flake8 .
   ```

5. Push changes:
   ```bash
   git push origin your-branch-name
   ```

6. Create pull request:
   - Use a clear title and description
   - Reference related issues
   - Include any necessary screenshots
   - List any breaking changes

## 🐛 Reporting Issues

When reporting issues, please include:

1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information:
   - Python version
   - Operating system
   - Package versions
   - GPU information (if relevant)

## 🎨 Style Guide

### Python Code Style
```python
# Good example
def process_video(
    input_path: str,
    output_path: str,
    duration: float = 60.0
) -> bool:
    """
    Process a video file with specified parameters.

    Args:
        input_path: Path to input video
        output_path: Path to save processed video
        duration: Video duration in seconds

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Implementation
        return True
    except Exception as e:
        logger.error(f"Video processing failed: {e}")
        return False
```

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues when applicable
- Use prefixes:
  - feat: New feature
  - fix: Bug fix
  - docs: Documentation
  - style: Code style
  - refactor: Code refactoring
  - test: Testing
  - chore: Maintenance

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [Docstring Conventions (PEP 257)](https://www.python.org/dev/peps/pep-0257/)
- [Git Commit Messages](https://chris.beams.io/posts/git-commit/)

## ❓ Questions?

Feel free to:
1. Open an issue for discussion
2. Join our community discussions
3. Contact maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
