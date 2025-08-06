# Restaurant API

A fully-featured Restaurant Management API built with Django REST Framework and Djoser + JWT Authentication.  
This project provides endpoints for managing menu items, orders, reservations, and user ratings with fine-grained permission control.

## Features

- JWT Authentication (via [Djoser](https://djoser.readthedocs.io/) and [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/))
- Menu Management: List, filter, and search menu items.
- User Ratings: Authenticated users can leave ratings and comments for menu items.
- Order Management: Customers can place orders; managers can update and manage all orders.
- Reservation System: Users can book reservations for a specific date and time; managers can view and manage all reservations.
- Role-Based Permissions:
  - Manager & AppOwner: Full access to all orders and reservations.
  - Delivery Crew: Access to assigned deliveries and status updates.
  - Customers: Can view and manage only their own orders, reservations, and ratings.
- Filtering & Search using django-filter and DRF SearchFilter.
- Pagination for large datasets.
- Validation: Prevents reservations from being made in the past.

---

## Technologies Used

- Python 3.13
- Django 5.2.4
- Django REST Framework
- Djoser
- SimpleJWT
- django-filter

---

## Installation

1. Clone the repository
   `bash
   git clone https://github.com/BehnamNahari/Restaurant_API.git
   cd gourmethub-api

2. Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt


4. Run migrations

python manage.py migrate


5. Create a superuser

python manage.py createsuperuser


6. Run the development server

python manage.py runserver




---

API Endpoints

Method Endpoint Description

GET /api/menu-items/ List menu items
GET /api/menu-items/{id} Retrieve a single menu item
GET/POST /api/ratings/ List or create ratings
GET/PATCH/DELETE /api/ratings/{id} Retrieve, update, or delete a rating
GET/POST /api/orders/ List or create orders
GET/PATCH/DELETE /api/orders/{id} Retrieve, update, or delete an order
GET/POST /api/reservations/ List or create reservations
GET/PATCH/DELETE /api/reservations/{id} Retrieve, update, or delete a reservation



---

Authentication

This API uses JWT Authentication.

1. Obtain token

POST /api/auth/jwt/create/

Request body:

{
  "username": "yourusername",
  "password": "yourpassword"
}


2. Use the token Add the token to the Authorization header:

Authorization: Bearer <access_token>




---

Running Tests

python manage.py test


---

License

This project is licensed under the MIT License. See the LICENSE file for details.

---
