Powerhouse Fitness (E-commerce)
Overview

Powerhouse Fitness is a full-stack e-commerce web application designed for gym equipment sales and management. The project demonstrates end-to-end development using Django, Bootstrap, and SQL, focusing on scalability, user accessibility, and secure role-based functionality. It provides a modern and responsive user experience while ensuring structured data handling on the backend.

Features
Role-Based Access: Controlled access for Admin, Staff, Vendor, and User roles.
Authentication: Secure login and registration system with session-based access.
Product Management: CRUD operations for adding, updating, and deleting products.
Shopping Cart: Add-to-cart functionality with dynamic updates and checkout simulation.
Responsive UI: Clean and mobile-friendly interface built with Bootstrap, AOS, and Boxicons.
Database Integration: SQL-based data storage for users, products, and orders.
SEO Optimization: Enhanced structure and metadata for better search visibility.
Tech Stack
Frontend: HTML, CSS, Bootstrap, JavaScript
Backend: Django Framework (Python)
Database: MySQL
Tools Used: VS Code, XAMPP, Git, GitHub
Installation and Setup
Clone the repository:
git clone https://github.com/AllenDarson/ecommerce_django.git

Navigate to the project directory:
cd powerhouse-fitness

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Open your browser and visit http://127.0.0.1:8000/
Usage
Admin can manage users, vendors, and products.
Vendors can add and manage their listed products.
Users can browse products, add to cart, and view purchase summaries.
Staff can assist in monitoring vendor operations.
Future Enhancements
Payment gateway integration
Order tracking system
Product reviews and ratings
Dashboard for analytics and reports

Author
Allen Darson C

This project was created for learning and demonstration purposes, focusing on secure, role-based full-stack web application development using Django
