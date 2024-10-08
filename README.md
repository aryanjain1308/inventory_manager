# Inventory Management System API

## Overview

The Inventory Management System API is a backend application built using Django Rest Framework (DRF) that allows users to manage inventory items efficiently. It supports CRUD (Create, Read, Update, Delete) operations on inventory items and utilizes JWT-based authentication for secure access. The API is integrated with PostgreSQL for data storage and Redis for caching frequently accessed items.

## Features

- User registration and authentication using JWT.
- CRUD operations for inventory items.
- Redis caching for improved performance.
- Comprehensive logging for debugging and monitoring.
- Unit tests to ensure functionality.

## Technologies Used

- Django
- Django Rest Framework
- PostgreSQL
- Redis
- Simple JWT

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Redis

### Setup Instructions

a. **Clone the repository:**

   'git clone https://github.com/aryanjain1308/inventory_manager.git'

   'cd core'

b. **Create and activate a virtual environment:**

   'python -m venv venv'
    # On Windows use 'venv\Scripts\activate'

c. **Install dependencies:**

   'pip install -r requirements.txt'

d. **Run migrations:**

   'python manage.py migrate'

e. **Start the Django development server:**

   'python manage.py runserver'
