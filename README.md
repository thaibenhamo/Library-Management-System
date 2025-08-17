# 📚 Library Management System

A Flask-based Library Management System that supports book inventory, user management, loan processing, and integration with the Google Books API.

## 📌 Table of Contents
- Features  
- Tech Stack  
- Project Structure  
- Getting Started  
- API Endpoints  
- Database Schema  
- Authentication  
- Future Improvements  

---

## 🚀 Features

### Core Functionality
- **User Management**: Registration, authentication, and user lookup  
- **Category Management**: Create, update, delete, and fetch book categories  
- **Author Management**: Automatically handle author creation during book import  
- **Book Management**: Add books from Google Books API with metadata handling  
- **Loan Management**: Issue and return books, track user loan history  
- **Book Copy Handling**: Handle multiple physical copies of the same book  

### Advanced Features
- **Google Books Integration**: Search and import books using external API  
- **Loan Statistics**: Track returned vs. unreturned loans  
- **Validation**: Regex-based manual validation for inputs   
- **Secure Password Handling**: Passwords hashed 

---

## 🛠️ Tech Stack

- **Backend Framework**: Flask  
- **ORM**: SQLAlchemy  
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)  
- **Authentication**: Manual session management  
- **API Consumption**: Google Books API  
- **Security**: Werkzeug (password hashing)  
- **Documentation Style**: PEP-8 + inline docstrings  

---

## 🗂️ Project Structure

```
├── config/                          # Configuration files
├── instance/
│   └── app.db                       # SQLite database file
├── models/                          # SQLAlchemy models
│   ├── Author_model.py
│   ├── book_model.py
│   ├── book_copy_model.py
│   ├── category_model.py
│   ├── loan_model.py
│   └── user_model.py
├── repositories/                   # Data access layer
│   ├── author_repository.py
│   ├── book_repository.py
│   ├── book_copy_repository.py
│   ├── category_repository.py
│   ├── loan_repository.py
│   └── user_repository.py
├── routes/                         # Flask route handlers
│   ├── auth_routes.py
│   ├── author_routes.py
│   ├── book_routes.py
│   ├── book_copy_routes.py
│   ├── category_routes.py
│   ├── loan_routes.py
│   ├── user_routes.py
│   ├── health_routes.py
│   └── export_routes.py
├── services/                       # Business logic layer
│   ├── auth_service.py
│   ├── author_service.py
│   ├── book_service.py
│   ├── book_copy_service.py
│   ├── category_service.py
│   ├── loan_service.py
│   ├── user_service.py
│   └── fill_books_service.py
├── utils/
│   └── password_utils.py           # Password hashing utilities
├── extensions.py                   # Flask extension bindings
├── app.py                          # Entry point of the application
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```


---

## 🏁 Getting Started

### Prerequisites
- Python 3.8+
- Flask & dependencies from `requirements.txt`

### Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd Library-Management-System
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   flask run
   ```

---

## 🔗 API Endpoints (Summary)

> These are just a few — full API documentation recommended using Swagger/Postman.

### User
- `POST /users/register`
- `POST /users/login`
- `GET /users/<id>`

### Category
- `GET /categories`
- `POST /categories/add`
- `PUT /categories/update/<id>`
- `DELETE /categories/delete/<id>`

### Book Import
- `POST /books/fetch` — Uses Google Books API to insert books by query

### Loans
- `POST /loans/create`
- `POST /loans/return/<loan_id>`
- `GET /loans/user/<user_id>`
- `GET /loans/stats`

---

## 🗃️ Database Schema

### User
- `id`, `username`, `password`, `email`

### Book
- `id`, `title`, `author_id`, `category_id`

### Author
- `id`, `name`

### Category
- `id`, `name`

### Loan
- `id`, `user_id`, `book_copy_id`, `loan_date`, `return_date`, `is_returned`

### BookCopy
- `id`, `book_id`, `available`

---

## 🔐 Authentication

- Manual session-style login (no JWT)
- Passwords are hashed using Werkzeug
- Validation using `re` (regex) in service layer

---

## 📈 Future Improvements

- JWT-based session authentication  
- Admin role management for category/book access control  
- Swagger/OpenAPI docs  
- Pagination & filtering  
- Testing suite using Pytest

