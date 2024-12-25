TMS (Training Management System)
Project Overview

The Training Management System (TMS) is a Django-based application designed to streamline the management of training activities. It integrates user account management, activity tracking, course management, and dynamic dashboards for an efficient training experience.
Branch Structure

    main: The primary branch and starting point for development.
    dashboard: Dedicated to dashboard-oriented components.
    bootstrap: Focused on integrating Bootstrap for responsive design.
    course-management: Handles all course-related functionalities.

Application Modules

    Accounts App:
        Models for user profiles (Student, Teacher, Staff, Parent) based on a common base profile.
        User authentication and management (login, signup, profile forms).

    Activities App:
        Tracks various activity types such as exercises, assignments, assessments, and projects.

    Course App:
        Manages courses, modules, tasks, and sessions.
        Admin feature for exporting data in CSV format.

    Dashboard App:
        Provides interactive dashboards and navigation systems.

Root Directory Structure

    Static Files: CSS, JavaScript, and other assets.
    Templates: HTML files for front-end rendering.
    README.md: Detailed project documentation.
    requirements.txt: List of Python dependencies.

Key Features

    Comprehensive user management.
    Activity tracking and analytics.
    Modular course management with session planning.
    Export functionality for admin use.
    Responsive design using Bootstrap.

Getting Started

    Clone the repository:

git clone https://github.com/username/predictive_model.git
cd predictive_model

Install dependencies:

pip install -r requirements.txt

Apply migrations and start the server:

    python manage.py migrate
    python manage.py runserver

    Access the application at http://localhost:8000.

Contributions

Contributions are welcome! Please submit a pull request or open an issue for suggestions and improvements.
License

This project is licensed under the MIT License.
