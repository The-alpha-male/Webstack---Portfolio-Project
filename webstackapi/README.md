# Final Webstack Portfolio Project

## Overview

The **Final Webstack Portfolio Project** is a comprehensive web application designed to showcase a full-stack solution. This project includes both a frontend and backend component, demonstrating skills in modern web development technologies.

### Backend Server

The backend server for this project is built using Python with FastAPI. It provides the API endpoints and business logic needed to support the frontend application.

#### Key Features

- **RESTful API**: Offers endpoints for CRUD operations and dynamic data fetching.
- **Authentication**: Implements user authentication and authorization.
- **Data Management**: Manages data persistence and retrieval, supporting operations on various data entities.
- **Scalability**: Designed with scalability in mind, capable of handling various loads.

#### Technologies Used

- **FastAPI**: For building the RESTful API.
- **SQLAlchemy**: For database management and ORM.
- **Docker**: For containerization and consistent development environments.
- **Uvicorn**: ASGI server for serving the FastAPI application.

## Prerequisites

Before you start, ensure you have the following installed:

- **Python**: [Version](https://www.python.org/downloads/)
- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Installation Guide](https://docs.docker.com/compose/install/)

## Setup

### 1. Create a Virtual Environment

In your project directory, create a virtual environment using `venv`:

```bash
python -m venv venv
```

### 2 2. Activate the Virtual Environment

**On Windows:**

venv\Scripts\activate

**On macOS and Linux:**

source venv/bin/activate

### 3. Install Project Dependencies

If your project has a requirements.txt file, install the dependencies with:

```bash
pip install -r requirements.txt
```

### 4. Build and Run Docker Containers

```bash
docker-compose up --build
```
