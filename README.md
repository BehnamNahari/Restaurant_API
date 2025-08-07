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

 Authentication (Djoser + JWT)

Method Endpoint Description

POST /auth/users/ Register a new user
POST /auth/jwt/create/ Obtain JWT access and refresh
POST /auth/jwt/refresh/ Refresh access token
POST /auth/jwt/verify/ Verify token
GET /auth/users/me/ Get current authenticated user




 Menu Items

Method Endpoint Description

GET /api/menu-items/ List all menu items
POST /api/menu-items/ Create new menu item (admin only)
GET /api/menu-items/{id}/ Retrieve a single menu item
PUT /api/menu-items/{id}/ Update menu item (admin only)
DELETE /api/menu-items/{id}/ Delete menu item (admin only)





 Orders

Method Endpoint Description

GET /api/orders/ List all orders (manager / user)
POST /api/orders/ Place a new order
GET /api/orders/{id}/ Retrieve a specific order
PUT /api/orders/{id}/ Update order (manager / delivery only)
DELETE /api/orders/{id}/ Cancel order (user or manager)





 Reservations

Method Endpoint Description

GET /api/reservations/ List all reservations (user / admin)
POST /api/reservations/ Create a new reservation
PUT /api/reservations/{id}/ Update reservation (user / admin)
DELETE /api/reservations/{id}/ Cancel reservation




 Ratings

Method Endpoint Description

GET /api/ratings/ List all ratings
POST /api/ratings/ Add new rating for a menu item
GET/PUT/DELETE /api/ratings/{id} 




 Notes:

Endpoints protected by JWT require Authorization: Bearer <access_token> in headers.

Group-based permissions control access for:

Manager – full control over menu, orders

Delivery Crew – can view/update delivery orders

Customers – can browse, order, reserve



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
