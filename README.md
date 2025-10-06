# Inventory Management System API

## Overview

This project is a backend-focused RESTful API built using Django and Django REST Framework (DRF) for managing warehouse inventory. It allows full CRUD operations on products, with built-in logic to handle stock quantities securely (e.g., preventing negative stock). The API includes dedicated endpoints for adding and removing stock, along with error handling for invalid operations. As a bonus feature, there's an endpoint to identify products below a configurable low-stock threshold.

This implementation demonstrates clean Django patterns, robust business logic, and adherence to REST principles. It's designed for the Associate Software Engineer (ASE) Challenge, emphasizing fundamentals like code quality, validation, and testing over unnecessary complexity.

**Tech Stack**:
- Backend: Django 5.0.4, Django REST Framework 3.15.1
- Database: SQLite (default; production-ready for PostgreSQL)
- Testing: Django's built-in TestCase with DRF's APIClient

## Features

- **Product CRUD**:
  - Create, read, update, and delete products with fields: `name` (required), `description` (optional), `stock_quantity` (non-negative integer), `low_stock_threshold` (bonus, default 10).
- **Inventory Management**:
  - `add_stock`: Increases stock by a positive integer quantity.
  - `remove_stock`: Decreases stock, errors (400) if insufficient.
- **Bonus**: `low_stock`: Lists products where `stock_quantity < low_stock_threshold`.
- **Validation & Errors**: Stock can't go negative; 400 for business errors (e.g., invalid quantity, insufficient stock); 404 for missing resources.
- **Unit Tests**: Coverage for stock operations, including edge cases (e.g., zero/negative quantity, over-removal).

## API Endpoints

| Method   | Endpoint                          | Description                          | Request Body Example                  |
|----------|-----------------------------------|--------------------------------------|---------------------------------------|
| **GET**  | `/api/products/`                  | List all products                    | N/A                                   |
| **POST** | `/api/products/`                  | Create a new product                 | `{"name": "Widget", "stock_quantity": 10}` |
| **GET**  | `/api/products/<id>/`             | Retrieve a single product            | N/A                                   |
| **PUT**  | `/api/products/<id>/`             | Full update of a product             | `{"name": "Updated Widget", "stock_quantity": 15}` |
| **PATCH**| `/api/products/<id>/`             | Partial update (e.g., stock only)    | `{"stock_quantity": 20}`              |
| **DELETE**| `/api/products/<id>/`           | Delete a product                     | N/A                                   |
| **POST** | `/api/products/<id>/add_stock/`   | Add to stock                         | `{"quantity": 5}`                     |
| **POST** | `/api/products/<id>/remove_stock/`| Remove from stock                    | `{"quantity": 3}`                     |
| **GET**  | `/api/products/low_stock/`        | List low-stock products (bonus)      | N/A                                   |

- **Base URL**: `http://127.0.0.1:8000`
- Test with Postman, curl, or DRF's browsable API (auto-generated at `/api/`).

Example curl for creating a product:
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "description": "A sample item", "stock_quantity": 10, "low_stock_threshold": 5}'
```

## Setup Instructions

### Prerequisites
- Python 3.8+ (recommended: 3.12)
- Git

### Step-by-Step Installation
1. **Clone the Repository**:
   ```
   git clone https://github.com/[your-username]/inventory-management-system-api.git
   cd inventory-management-system-api
   ```

2. **Create and Activate Virtual Environment**:
   ```
   python -m venv venv
   ```
   - Activate:
     - macOS/Linux: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`

3. **Install Dependencies**:
   Create `requirements.txt` if not present (or use the one in the repo):
   ```
   django==5.0.4
   djangorestframework==3.15.1
   ```
   Then:
   ```
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser** (for Django Admin access):
   ```
   python manage.py createsuperuser
   ```
   - Use this to manually add sample products via `http://127.0.0.1:8000/admin/`.

6. **Run the Development Server**:
   ```
   python manage.py runserver
   ```
   - API root: `http://127.0.0.1:8000/api/`
   - Admin: `http://127.0.0.1:8000/admin/`

### Sample Data
- After setup, use the POST `/api/products/` endpoint or admin to create test products (e.g., one with low stock for the bonus endpoint).

## Running Tests

Tests are in `warehouse/tests.py` and focus on stock logic (add/remove, validations, low-stock query).

1. Ensure virtual environment is activated and server is not running.
2. Run:
   ```
   python manage.py test warehouse
   ```
   - Output example:
     ```
     Creating test database for alias 'default'...
     ...
     Ran X tests in Ys
     OK
     Destroying test database for alias 'default'...
     ```
   - All tests should pass. Coverage includes:
     - Successful add/remove stock.
     - Errors for invalid quantity (negative/zero).
     - Insufficient stock prevention.
     - Low-stock filtering.

For more verbose output: `python manage.py test warehouse --verbosity=2`.

## Project Structure

```
inventory-management-system-api/
├── inventory_api/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── warehouse/              # Core app
│   ├── models.py          # Product model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views (ViewSet)
│   ├── urls.py            # Router for endpoints
│   ├── tests.py           # Unit tests
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
```

## Assumptions and Design Choices

- **Database**: SQLite for simplicity in development; no issues for this scope. For production, update `settings.py` DATABASES to PostgreSQL/MySQL.
- **Authentication/Authorization**: Skipped to focus on core logic (as per challenge). Could add DRF's `TokenAuthentication` or JWT via `rest_framework_simplejwt`.
- **Validation Layers**: Multi-tiered (model fields, serializer, view methods) for defense-in-depth. E.g., `PositiveIntegerField` blocks negatives at DB, views add business checks.
- **Stock Endpoints**: Custom `@action` methods (POST) for specificity—easier to test/validate than overloading PUT/PATCH. Quantity must be positive integer to enforce safe operations.
- **Bonus Feature**: Implemented `low_stock` with `F('low_stock_threshold')` for atomic, efficient queries (avoids race conditions in concurrent updates).
- **Error Handling**: Custom 400 responses with descriptive messages (e.g., "Quantity must be a positive integer.") for better UX in API clients.
- **No Advanced Features**: Omitted pagination, search, or rate-limiting to prioritize fundamentals. DRF settings can enable them easily.
- **Testing Focus**: Unit/integration tests target high-risk areas (stock mutations). 100% pass rate; could expand with pytest for more coverage.
- **Deployment**: Local-only; for Heroku/Vercel, add `Procfile` and env vars.

## Contributing & Contact

This is a challenge submission, but PRs welcome! Fork, branch, and submit. Questions? Reach out via GitHub issues or [your-email@example.com].

**Built for the Associate Software Engineer Challenge – October 2025**  
By [Your Name] | [Your LinkedIn/GitHub] | [Loom Demo Video Link if applicable]
