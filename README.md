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
- **Database**: PostgreSQL   
- **Authentication**: Manual session management  
- **API Consumption**: Google Books API  
- **Security**: bcrypt (password hashing)  

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
│   ├── password_utils.py           # Password hashing utilities
│   ├── export_utils.py 
│   └── authz.py
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

# 📖 Library Management System – API Documentation

Base URL: `http://127.0.0.1:5000/api`

---

## 🩺 Health
- **GET `/health`**  
  Returns service health.  
  **Response:**  
  ```json
  { "status": "ok" }
  ```

---

## 🔐 Auth
- **POST `/auth/login`**  
  ```json
  { "username": "john123", "password": "Password@123" }
  ```
  **Response:**  
  ```json
  {
    "access_token": "<JWT>",
    "user": { "id": 1, "username": "john123", "email": "john@example.com" }
  }
  ```

- **POST `/auth/logout`**  
  **Response:**  
  ```json
  { "message": "Logged out successfully", "success": true }
  ```

---

## 👤 Users
- **POST `/users`** – create user  
  ```json
  { "username": "john123", "password": "Password@123", "email": "john@example.com" }
  ```

- **GET `/users`** – list all users  
- **GET `/users/<id>`** – get user by id  
- **GET `/users/username/<username>`** – get user by username  
- **GET `/users/email/<email>`** – get user by email  

- **PUT `/users/<id>`** – update user  
  ```json
  { "email": "new@example.com", "password": "NewPass@123" }
  ```

- **DELETE `/users/<id>`** – delete user  

---

## ✍ Authors
- **POST `/authors`** – create author  
  ```json
  { "name": "Isaac Asimov" }
  ```

- **GET `/authors`** – list all authors  
- **GET `/authors/<id>`** – get author by id  

- **PUT `/authors/<id>`** – update author  
  ```json
  { "name": "Arthur C. Clarke" }
  ```

- **DELETE `/authors/<id>`** – delete author  

---

## 📚 Categories
- **POST `/categories`** – create category  
  ```json
  { "name": "Science Fiction" }
  ```

- **GET `/categories`** – list all categories  
- **GET `/categories/<id>`** – get category by id  

- **PUT `/categories/<id>`** – update category  
  ```json
  { "name": "Sci-Fi" }
  ```

- **DELETE `/categories/<id>`** – delete category  

---

## 📖 Books
- **GET `/books`** – list all books  

- **POST `/books`** – create book  
  ```json
  { "title": "Dune", "author_id": 3, "category_id": 1 }
  ```

- **GET `/books/<id>`** – get book by id  

- **PUT `/books/<id>`** – update book  
  ```json
  { "title": "Dune (Revised)" }
  ```

- **DELETE `/books/<id>`** – delete book  

- **POST `/books/fill_external`** – import via Google Books  
  ```json
  { "query": "science fiction", "limit": 10 }
  ```

- **GET `/books/by-title/<title>`** – find book by title  

---

## 📕 Book Copies
- **GET `/book_copies`** – list all book copies  

- **POST `/book_copies`** – create book copy  

- **GET `/book_copies/<id>`** – get book copy  

- **PUT `/book_copies/<id>`** – update book copy  

- **DELETE `/book_copies/<id>`** – delete book copy  

- **GET `/book_copies/availability`** – list available copies (counts per book)  

---

## 📑 Loans
- **GET `/loans`** – list all loans  

- **POST `/loans`** – create loan
- **PUT `/loans/<loan_id>/return`** – return a loan  
- **GET `/loans/<loan_id>`** – get loan  
- **GET `/loans/user/<user_id>`** – get user’s loan history  
- **GET `/loans/stats`** – loan statistics  

---

## 📤 Export (Excel)
- **GET `/export/books.xlsx`**  
- **GET `/export/authors.xlsx`**  
- **GET `/export/categories.xlsx`**  
- **GET `/export/book_copies.xlsx`**  
- **GET `/export/loans.xlsx`**  
- **GET `/export/users.xlsx`**  
- **GET `/export/all.xlsx`** – all entities in one workbook

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

