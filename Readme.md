# Assessment API – FastAPI + MongoDB (Beanie) + JWT Auth
This project is a backend assessment built using FastAPI, MongoDB, Beanie ODM, and JWT authentication.
It includes secure user registration, login, and protected CRUD operations.

## Features
🔐 Authentication
- User registration with hashed passwords (bcrypt or argon2)
- Email-based login
- JWT-based authentication (Bearer token)
- Protected API routes requiring valid JWT

👤 User Management
- Create user
- Get all users
- Get user by ID
- Update user
- Delete user

🗄 Database
- MongoDB
- Beanie ODM for async document modeling
- Automatic timestamping (created_at, updated_at)

⚙️ FastAPI
- Highly performant Python web framework
- Built-in validation, interactive Swagger UI
- CORS enabled


## Installation
- git clone "https://github.com/HimanshuXDevX/Assesment.git"
- python -m venv venv
- venv/Scripts/activate
- pip install -r requirements.txt

## API endppoints
- GET /health
- POST /register
- POST /login
- GET /users
- GET /users/{id}
- PUT /users/{id}
- DELETE /users/{id}