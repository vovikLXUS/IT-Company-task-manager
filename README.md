# 💻 IT Company Task Manager

A web application designed for tracking tasks, organizing team workload, and managing roles within an IT company, built with **Django** and styled with **Bootstrap 5**.

---

## 📌 Project Overview

### 🎯 Topic
An internal task management and team collaboration system for an IT company (Task Tracking & Team Management System).

### 🚀 Purpose & Goal
To provide a clean, reliable, and user-friendly platform for developers and project managers to:
* Categorize and prioritize tasks by urgency and technical type.
* Assign tasks to individual developers or multi-disciplinary teams.
* Monitor deadlines and task completion status in real-time.
* Manage company positions, worker profiles, and role assignments.
* Securely authenticate and register team members with granular permission controls.

---

## ✨ Features & Capabilities

### 🔐 Authentication & Accounts
* **User Registration:** Simple, intuitive registration with `username`, `email`, `first_name`, `last_name`, and company `position`. Automatically signs the new user in upon registration.
* **Dual-mode Login:** Seamless login via **either username or email address** (case-insensitive) using a custom authentication backend (`EmailOrUsernameModelBackend`).
* **Session Management:** Secure login, logout, and session-based page visit counter.

### 👤 Profile & Worker Management
* **Worker Profiles:** Detailed profile views with personal info and active assigned tasks.
* **Granular Profile Updates:** Workers can update all their personal details (`username`, `email`, `first_name`, `last_name`, `position`).
* **Role-Based Access Control:** Strict permission check powered by `UserPassesTestMixin` — workers can only update their own profile, whereas administrators (`is_staff` / superusers) can update any worker.
* **Team Directory:** Paginated list of all team members with username search and role badges.

### 📋 Task Management
* **Task Catalog & Search:** Paginated overview of all tasks with real-time name search filtering.
* **Task Details & Direct Toggle:** Dedicated task view displaying urgency badges, deadlines, assignees, and a one-click button to self-assign or unassign from the task.
* **Complete Task CRUD:** Create, read, update, and delete tasks with multiple assignee selection.

### 🏷️ Positions & Task Types
* **Positions Management:** Manage job roles (`Developer`, `QA`, `Project Manager`, `DevOps`, `Designer`, etc.) with search and full CRUD operations.
* **Task Types Management:** Organize work items by category (`New Feature`, `Bug`, `Refactoring`, `QA`, etc.) with search and full CRUD operations.

### 🎨 Modern UI & Global Navigation
* **Quick Repo Link:** Header on the home page features a direct GitHub repository shortcut opposite to the main title.
* **Collapsible / Fixed Sidebar:** Displays user avatar, active status, quick "Edit profile" button, navigation links, and logout trigger.
* **Global Footer:** Modern footer on all pages featuring social media links (Instagram, LinkedIn, GitHub, Telegram), author attribution (*"Created by Volodymyr Datsyshyn"*), and educational support link (*"Supported by Mate Academy"*).

---

## 📸 Demo

### 🔐 Authentication
* **Login Page (Username or Email):**
  ![Login Page](assets/demo_photos/login_page.png)

* **Register Page:**
  ![Register Page](assets/demo_photos/register_page.png)

### 🏠 Dashboard
* **Home Page with Statistics, GitHub Repo Link & Global Footer:**
  ![Dashboard](assets/demo_photos/home_page.png)

### 📋 Task Management
* **Tasks List & Filtering:**
  ![Tasks List](assets/demo_photos/tasks_page.png)

* **Create Task:**
  ![Create Task](assets/demo_photos/create_task_page.png)

### 👥 Team & Worker Management
* **Workers List:**
  ![Workers List](assets/demo_photos/workers_page.png)

* **Worker Profile & Assigned Tasks:**
  ![Worker Detailed View](assets/demo_photos/worker_detailed_page.png)

* **Current User Profile View:**
  ![User Profile Page](assets/demo_photos/user_page.png)

* **Update Profile Page (Full Field Editing with Permissions):**
  ![Update Profile](assets/demo_photos/update_profile_page.png)

* **Create Worker (Admin / Staff Workflow):**
  ![Create Worker](assets/demo_photos/create_worker_page.png)

### 🏷️ Positions & Task Types
* **Positions List:**
  ![Positions](assets/demo_photos/positions_page.png)

* **Create Position:**
  ![Create Position](assets/demo_photos/create_position_page.png)

* **Task Types List:**
  ![Task Types](assets/demo_photos/task_types_page.png)

* **Create Task Type:**
  ![Create Task Type](assets/demo_photos/create_task_type_page.png)

---

## 🛠 Technologies Used

* **Backend:**
  * [Python 3.12+](https://www.python.org/)
  * [Django 6.1+](https://www.djangoproject.com/) — High-level Python web framework
  * [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/) & [Crispy Bootstrap 5](https://github.com/django-crispy-forms/crispy-bootstrap5) — Elegant form rendering with Bootstrap 5
  * [WhiteNoise](http://whitenoise.evans.io/) — Efficient static file serving for production
  * [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/) — Performance profiling and query optimization
  * Custom Authentication Backend (`EmailOrUsernameModelBackend`) — Dual username/email authentication
* **Database:**
  * [SQLite](https://www.sqlite.org/) (used by default for local development, easily configurable for PostgreSQL)
* **Frontend:**
  * [Bootstrap 5.3](https://getbootstrap.com/) — Responsive CSS/JS framework
  * [Bootstrap Icons](https://icons.getbootstrap.com/) — Modern vector icon library
  * [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) — Modern typography (Google Fonts)
  * Custom CSS stylesheet ([`styles.css`](static/css/styles.css))
* **Code Quality & Testing:**
  * Automated Test Suite with **37 test cases** covering models, forms, views, auth, and permissions
  * [Flake8](https://flake8.pycqa.org/) — PEP 8 style guide enforcement
  * [Black](https://black.readthedocs.io/) — Python code formatter

---

## 🗄️ Database Structure

The relationship between the system entities is illustrated below:

![Database Structure](assets/db_structure.png)

### 📊 Entity Descriptions

1. **`Position`**:
   * Represents job roles within the company (`Developer`, `QA`, `Project Manager`, `DevOps`, `Designer`, etc.).
   * `name`: Unique name of the position.
2. **`TaskType`**:
   * Categorizes work items (`New Feature`, `Bug`, `Refactoring`, `Breaking change`, `QA`).
   * `name`: Name of the task type.
3. **`Worker`**:
   * Extends Django's `AbstractUser` model.
   * Attributes: `username`, `email`, `first_name`, `last_name`, `password`.
   * `position`: Foreign key (`ForeignKey`) referencing the `Position` model (Many-to-One).
4. **`Task`**:
   * Core work unit with `name`, `description`, `deadline`, and `is_completed` fields.
   * `priority`: Choices between `Urgent`, `High`, `Medium`, and `Low`.
   * `task_type`: Foreign key (`ForeignKey`) referencing `TaskType` (Many-to-One).
   * `assignees`: Many-to-Many relationship with `Worker` (tasks can have multiple assignees).

---

## 🏛️ Project Architecture

The project follows Django's standard **MTV (Model - Template - View)** pattern:

```text
IT-Company-task-manager/
├── assets/
│   ├── db_structure.png         # Database structure diagram
│   └── demo_photos/             # Application screenshots (14 pages)
│       ├── create_position_page.png
│       ├── create_task_page.png
│       ├── create_task_type_page.png
│       ├── create_worker_page.png
│       ├── home_page.png
│       ├── login_page.png
│       ├── positions_page.png
│       ├── register_page.png
│       ├── task_types_page.png
│       ├── tasks_page.png
│       ├── update_profile_page.png
│       ├── user_page.png
│       ├── worker_detailed_page.png
│       └── workers_page.png
├── IT_company_task_manager/     # Main project configuration
│   ├── settings/                
│   │   ├── __init__.py
│   │   ├── base.py              # Base settings (apps, auth backends, crispy)
│   │   ├── dev.py               # Development settings
│   │   └── prod.py              # Production settings
│   ├── __init__.py
│   ├── asgi.py          
│   ├── urls.py                  # Root URL configuration (login, register, admin)
│   └── wsgi.py
├── tasks/                       # Core task management application
│   ├── migrations/              # Database migration history
│   ├── admin.py                 # Admin site registrations
│   ├── apps.py                  # Application configuration
│   ├── backends.py              # Custom auth backend (username or email login)
│   ├── forms.py                 # Forms for validation, auth, and filtering
│   ├── models.py                # Database models (Task, Worker, Position, TaskType)
│   ├── tests/                   # Automated test suite (37 tests)
│   │   ├── test_admin.py
│   │   ├── test_forms.py
│   │   ├── test_models.py
│   │   └── test_views.py
│   ├── urls.py                  # App-specific URL routes
│   └── views.py                 # Class-Based Views for CRUD operations & auth
├── templates/                   # HTML templates
│   ├── base.html                # Base layout with sidebar, footer, and styles
│   ├── includes/                # Reusable partials
│   │   ├── footer.html          # Global footer with social links and credits
│   │   ├── pagination.html      # Pagination controls
│   │   └── sidebar.html         # Navigation sidebar with user card & edit profile
│   ├── registration/            # Authentication templates
│   │   ├── logged_out.html      # Logout confirmation
│   │   ├── login.html           # Login with username or email
│   │   └── register.html        # User registration form
│   └── tasks/                   # Views for tasks, workers, positions, task types
├── static/                      # Static assets
│   └── css/
│       └── styles.css           # Custom styling and color scheme
├── staticfiles/                 # Collected static assets
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── README.md                    # Project documentation
└── manage.py                    # Django management script
```

### 🔑 Key Architectural Highlights:
* **Class-Based Views (CBVs):** All CRUD workflows utilize Django's `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView`.
* **Custom Authentication Backend:** `EmailOrUsernameModelBackend` enables users to authenticate using either their username or email address.
* **Access Control & Permissions:** Protected views enforce authentication with `LoginRequiredMixin`. `WorkerUpdateView` enforces role-based access via `UserPassesTestMixin`, guaranteeing that users can only modify their own profile while administrators retain full modification rights.
* **Query Optimization:** Efficient database querying utilizing `select_related` for ForeignKeys (`task_type`, `position`) and `prefetch_related` for ManyToMany relationships (`assignees`, `assigned_tasks`) to eliminate N+1 query bottlenecks.
* **Comprehensive Testing:** 37 automated unit and integration tests covering models, forms, access control, registration, and views.

---

## ⚡ Local Setup & Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/vovikLXUS/IT-Company-task-manager.git
cd IT-Company-task-manager
```

### 2. Create and activate a virtual environment

* **Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file from `.env.example` (or configure your own `SECRET_KEY` and `DEBUG`):
* **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
* **Linux / macOS / Git Bash:**
  ```bash
  cp .env.example .env
  ```

### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (Administrator)
```bash
python manage.py createsuperuser
```
*(Follow the prompt to provide a `username`, `email`, and `password`).*

### 7. Run test suite
```bash
python manage.py test
```

### 8. Start the development server
```bash
python manage.py runserver
```

Once running, access the application in your browser:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

The Django Admin panel is accessible at:
👉 **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**
