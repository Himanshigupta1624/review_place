# Review Place API

A Django REST API for managing user reviews of places. Users can register, login, add reviews for places, search for places by name and rating, and view detailed information about places with all their reviews.

## Features

- **User Management**
  - User registration with name and phone number
  - Token-based authentication
  - Unique phone number constraint

- **Place Management**
  - Automatic place creation when adding reviews
  - Case-insensitive unique constraint on name + address
  - Search places by name (partial/exact match)
  - Filter places by minimum average rating

- **Review System**
  - Add reviews with 1-5 star ratings
  - One review per user per place
  - View all reviews for a place
  - User's own review appears first in detail view
  - Reviews sorted by newest first

## Tech Stack

- **Backend**: Django 6.0
- **API Framework**: Django REST Framework
- **Database**: SQLite (default)
- **Authentication**: Token-based authentication
- **Python Version**: 3.13.9

## Requirements

- Python 3.13+
- Django 6.0
- Django REST Framework
- Faker (for seed data)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd review_place
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install django djangorestframework faker
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:
- Name
- Phone number
- Password

### 7. Seed Sample Data (Optional)

```bash
python manage.py seed_data
```

This creates:
- 10 sample users
- 30 sample places
- Random reviews for each place

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. Register User

**Endpoint:** `POST /api/register/`

**Authentication:** None required

**Request Body:**
```json
{
    "name": "John Doe",
    "phone_number": "1234567890"
}
```

**Response (201):**
```json
{
    "token": "abc123...",
    "user_id": 1,
    "name": "John Doe",
    "phone_number": "1234567890"
}
```

### 2. Login

**Endpoint:** `POST /api/login/`

**Authentication:** None required

**Request Body:**
```json
{
    "phone_number": "1234567890"
}
```

**Response (200):**
```json
{
    "token": "abc123...",
    "user_id": 1,
    "name": "John Doe",
    "phone_number": "1234567890"
}
```

### 3. Add Review

**Endpoint:** `POST /api/add-review/`

**Authentication:** Required (Token)

**Headers:**
```
Authorization: Token <your_token_here>
```

**Request Body:**
```json
{
    "place_name": "Central Park",
    "place_address": "New York, NY",
    "rating": 5,
    "text": "Beautiful park with lots of greenery!"
}
```

**Response (201):**
```json
{
    "id": "review.id",
    "place_id": 1,
    "place_name": "Central Park",
    "rating": 5,
    "text": "Beautiful park with lots of greenery!",
    "created_at": "2025-12-28T10:30:00Z"
}
```

**Notes:**
- If a place with the exact name and address exists, the review is added to it
- Otherwise, a new place is created
- Users can only submit one review per place

### 4. Search Places

**Endpoint:** `GET /api/places/`

**Authentication:** Required (Token)

**Headers:**
```
Authorization: Token <your_token_here>
```

**Query Parameters:**
- `name` (optional): Search by place name (partial/exact match)
- `min_rating` (optional): Minimum average rating filter

**Examples:**

Search all places:
```
GET /api/places/
```

Search by name:
```
GET /api/places/?name=park
```

Search by minimum rating:
```
GET /api/places/?min_rating=4
```

Combined search:
```
GET /api/places/?name=park&min_rating=4
```

**Response (200):**
```json
[
    {
        "id": 1,
        "name": "Central Park",
        "average_rating": 4.5
    },
    {
        "id": 2,
        "name": "City Park",
        "average_rating": 4.2
    }
]
```

**Notes:**
- Exact name matches appear first
- Then partial matches (case-insensitive)
- Results are ordered alphabetically
- Average rating is rounded to 2 decimal places

### 5. Place Details

**Endpoint:** `GET /api/places/<place_id>/`

**Authentication:** Required (Token)

**Headers:**
```
Authorization: Token <your_token_here>
```

**Example:**
```
GET /api/places/1/
```

**Response (200):**
```json
{
    "id": 1,
    "name": "Central Park",
    "address": "New York, NY",
    "average_rating": 4.5,
    "reviews": [
        {
            "id": 1,
            "user_name": "John Doe",
            "rating": 5,
            "text": "Beautiful park!",
            "created_at": "2025-12-28T10:30:00Z"
        },
        {
            "id": 2,
            "user_name": "Jane Smith",
            "rating": 4,
            "text": "Nice place to visit",
            "created_at": "2025-12-27T15:20:00Z"
        }
    ]
}
```

**Notes:**
- Current user's review appears first (if exists)
- Other reviews sorted by newest first
- Shows all place details with complete review list

## Database Schema

### User Model
- `name`: CharField (max 100 characters)
- `phone_number`: CharField (max 12 characters, unique, indexed)
- `created_by`: DateTimeField (auto-generated)
- `is_staff`: BooleanField (default: False)
- `is_active`: BooleanField (default: True)
- `password`: CharField (hashed)

### Place Model
- `name`: CharField (max 255 characters, indexed)
- `address`: TextField
- `created_at`: DateTimeField (auto-generated)
- **Constraint**: Unique combination of (name, address) - case-insensitive

### Review Model
- `user`: ForeignKey to User
- `place`: ForeignKey to Place
- `rating`: IntegerField (1-5, validated)
- `text`: TextField
- `created_at`: DateTimeField (auto-generated)
- **Constraint**: Unique combination of (user, place)
- **Ordering**: Newest first by default

## Testing with Postman

### Setup Collection

1. Create a new Postman collection named "Review Place API"
2. Set base URL variable: `{{base_url}}` = `http://localhost:8000/api`

### Test Flow

1. **Register User 1**
   - POST `{{base_url}}/register/`
   - Save token as `{{token_user1}}`

2. **Register User 2**
   - POST `{{base_url}}/register/`
   - Save token as `{{token_user2}}`

3. **User 1 Adds Review**
   - POST `{{base_url}}/add-review/`
   - Header: `Authorization: Token {{token_user1}}`

4. **Search Places**
   - GET `{{base_url}}/places/`
   - Header: `Authorization: Token {{token_user1}}`

5. **View Place Details**
   - GET `{{base_url}}/places/1/`
   - Header: `Authorization: Token {{token_user1}}`

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Features:
- Manage users, places, and reviews
- Custom user admin with phone number authentication
- View and edit all database records

## Project Structure

```
review_place/
├── manage.py
├── db.sqlite3
├── README.md
├── review_place/          # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── reviews_api/           # Main app
    ├── __init__.py
    ├── admin.py           # Admin configurations
    ├── apps.py
    ├── models.py          # User, Place, Review models
    ├── serializers.py     # DRF serializers
    ├── views.py           # API views
    ├── urls.py            # API URL patterns
    ├── tests.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py  # Sample data generator
    └── migrations/
```

