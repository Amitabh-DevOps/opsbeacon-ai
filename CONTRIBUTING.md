# Contributing to OpsBeacon AI

First off, thank you for considering contributing to OpsBeacon AI! We welcome contributions from everyone.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create a GitHub issue and include:
* A clear description of the issue.
* Steps to reproduce the bug.
* Expected vs actual behavior.
* Version information (Python, SAM CLI, OS).

### Suggesting Enhancements
We welcome ideas for new features or improvements. Please open an issue to discuss your ideas before writing code.

### Pull Requests
1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/my-cool-feature`
3. Implement your changes. Make sure to write unit tests.
4. Run formatting and linting check scripts:
   ```bash
   black --check src tests
   ruff check src tests
   pytest
   ```
5. Commit your changes with clear, descriptive commit messages.
6. Push to your branch and open a Pull Request.

## Coding Style

* Follow PEP 8 guidelines.
* Use type hints for all function arguments and return types.
* Write docstrings for all modules, classes, and methods.
* Keep functions small, modular, and focused.
