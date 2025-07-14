# tests/ - Project Test Suite

This directory contains test cases for validating the functionality, security, and stability of this project.

## Running the Tests

### Prerequisites

- Install dependencies
```bash
pip install -r requirements.txt
````
- Add application base URL to your .env file (BASE_URL)
- Ensure that your database is running

### Run All Tests
```bash
pytest tests/
```

### Folder Structure

tests/
├── __init__.py
├── test_auth.py
├── test_projects.py
├── test_services.py
├── test_users.py
└── conftest.py 