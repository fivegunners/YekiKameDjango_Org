# Django Project Setup Guide

## Prerequisites

1. **Python**: Make sure Python 3.x is installed.
2. **pip**: The pip package manager.
3. **virtualenv** (optional): To create a virtual environment (recommended).

## Project Setup

### 1. Clone The Repository

First, clone the project:

```bash
git clone <URL-REPOSITORY>
cd <project-name>
```

### 2. Create and Activate a Virtual Environment

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Linux and macOS
venv\Scripts\activate     # For Windows
```

### 3. Install Packages

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

If there are any environment configurations (like a `.env` file), set them up as needed.

### 5. Database Migrations

To create database tables, run the migration commands:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the project with the following command:

```bash
python manage.py runserver
```

The project is now accessible at [http://localhost:8000](http://localhost:8000).

## Tests

To run the tests, use the following command:

```bash
python manage.py test
```

To run the the specifics tests, use the following command:

```bash
python manage.py test Eventapp.tests
```

## Additional Notes

- **Create a Superuser**: To create an admin account, use the command:
  ```bash
  python manage.py createsuperuser
  ```

- **GraphQL Support**: This project includes GraphQL capabilities, which can be accessed at `/graphql/`.

workflow test44
