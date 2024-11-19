# Blog Application - Flask Full-Stack Project

A simple blog application built using **Flask** for the backend and **HTML/Bootstrap** for the frontend. The application features user management with MySQL as the database and includes functionalities like user registration, login with password encryption, and a clean, responsive UI.

---

## Features

### Backend
- **User Authentication**: Registration, login, and secure password storage.
- **Database Integration**: Uses MySQL for managing users and blog posts.
- **Flask Framework**: Entire backend is written in Python using Flask.
- **CRUD Operations**: Create, read, update, and delete blog posts (TODO).

### Frontend
- **Responsive Design**: Built with HTML and Bootstrap for modern, mobile-friendly layouts.
- **Dynamic Content**: Displays user-specific content and blog posts.

---

## Prerequisites

- **Python 3.7+**
- **MySQL Server**
- **pipenv** or **virtualenv** (optional, for virtual environments)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blog-flask-app.git
   cd blog-flask-app
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database named `blog_app` (or as specified in your config).
   - Update the database configuration in the `config.py` file:
     ```python
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/blog_app'
     ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

7. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

---


---

## Future Enhancements

- Add support for social media authentication (e.g., Google, Facebook).
- Implement a WYSIWYG editor for creating blog posts.
- Add a comments section for blog posts.
- Enhance security with rate limiting and user roles.

---

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-WTF
- **Frontend**: HTML, Bootstrap, JavaScript
- **Database**: MySQL
- **Authentication**: Flask-Login, Flask-Bcrypt

---

## Screenshots
TODO
1. **Homepage**
   ![Homepage](path/to/homepage-screenshot.png)

2. **Login Page**
   ![Login Page](path/to/login-page-screenshot.png)

3. **Dashboard**
   ![Dashboard](path/to/dashboard-screenshot.png)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any questions or suggestions, feel free to contact me:

- **GitHub**: [mart-dore](https://github.com/mart-dore)
