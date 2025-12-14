# FUDiscover - Departmental Final Year Project Repository

**FUDiscover** is a digital archive for the Computer Science department at Federal University Dutse. It solves the problem of project duplication and lost hard copies by providing a searchable, digital repository for final year projects.

![FUDiscover Hero](media/FUD%20main%20gate.png)

## 🚀 Features

-   **Searchable Database**: Students can search past projects by Title, Abstract, Keywords, Supervisor, or Year.
-   **Plagiarism Prevention**: 
    -   Basic "Local" plagiarism check using Levenshtein Distance (Title) and Cosine Similarity (Abstract).
    -   Flags submissions that are too similar to existing approved projects.
-   **Student Profile**: View your submission status and history.
-   **Upload Portal**: Supports PDF documentation and Source Code (ZIP) or GitHub Links.
-   **Admin Dashboard**: Supervisors/Admins can review and approve projects before they go live.

## 🛠️ Tech Stack

-   **Backend**: Python (Django 5.0)
-   **Database**: SQLite (Development) / PostgreSQL (Production ready)
-   **Frontend**: Django Template Language + Custom CSS (Glassmorphism UI)
-   **Plagiarism Logic**: `python-levenshtein`, `scikit-learn`

## 📦 Installation (Local Development)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/FUDiscover.git
    cd FUDiscover
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

4.  **Create Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run Server**
    ```bash
    python manage.py runserver
    ```

6.  **Access App**: Visit `http://127.0.0.1:8000`

## 🌍 Deployment (Render)

This project is configured for deployment on **Render**.

1.  Push to GitHub.
2.  Create a new Web Service on Render.
3.  Connect your repository.
4.  **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
5.  **Start Command**: `gunicorn fudiscover.wsgi`
6.  **Env Vars**: Set `PYTHON_VERSION` (3.13.5), `SECRET_KEY`, and `DEBUG` (False).

## 📄 License
Federal University Dutse - Computer Science Department.
