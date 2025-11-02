# Project Setup and Guide

This guide provides instructions for setting up and running the Ai-vehicle-detection project.

## 1. Project Setup

### a. Python Virtual Environment

To isolate project dependencies, it's recommended to use a Python virtual environment.

*   **Activate the virtual environment:**

    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```

    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```

### b. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## 2. Database Setup

The project uses a database to store information. Run the following commands to set up the database schema.

*   **Create migrations:**
    ```bash
    python manage.py makemigrations accounts detections tolls
    ```

*   **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

## 3. Running the Application

### a. Build Tailwind CSS

The project uses Tailwind CSS for styling. Before running the server, you need to build the CSS file.

*   **Navigate to the `tailwind_build` directory:**
    ```bash
    cd tailwind_build
    ```

*   **Run the Tailwind CSS build command:**
    ```bash
    npx tailwindcss -i input.css -o ../apps/ui/static/css/styles.css
    ```
    *You may need to run `npm install` first if you don't have the dependencies.*

### b. Run the Django Server

Once the setup is complete, you can run the Django development server.

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## 4. Creating an Admin User

You can create an admin user to access the admin dashboard.

### a. Using Sample Credentials

A sample admin user can be used for quick access:

*   **Username:** `admin01`
*   **Password:** `adminpass01`

### b. Creating a new Admin User

You can create a new admin user via the Django shell.

*   **Open the Django shell:**
    ```bash
    python manage.py shell
    ```

*   **Run the following Python code in the shell:**

    ```python
    from apps.accounts.models import CustomUser

    # Replace with your desired username, email, and password
    username = 'admin01'
    email = 'admin01@example.com'
    password = 'adminpass01'

    if not CustomUser.objects.filter(username=username).exists():
        admin_user = CustomUser(
            username=username,
            email=email,
            role='admin'
        )
        admin_user.set_password(password)
        admin_user.save()
        print(f"Admin user '{admin_user.username}' created successfully.")
    else:
        print(f"User '{username}' already exists.")
    ```
