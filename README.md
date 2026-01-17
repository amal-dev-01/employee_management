# 🧩 Dynamic Custom Form & Employee Management System

A **Django application** that allows admins to create **dynamic custom forms**, define fields at runtime, and store **employee data** against those forms. The project supports **JWT authentication**, advanced **search**, and **REST APIs using Django REST Framework (APIView)**.

---

## 🚀 Features

### 🔐 Authentication & Security

* Custom `User` model (email as username)
* JWT Authentication (Login / Refresh / Protected APIs)
* Transaction‑safe database operations

### 🧩 Dynamic Forms

* Create custom forms at runtime
* Add multiple fields using **formsets**
* Supported field types:

  * text
  * number
  * date
  * email
  * password
* Field‑level validation based on field type

### 👥 Employee Management

* Assign employees to a custom form
* Store dynamic values per field
* Search employees by **field label & value** (case‑insensitive)
* Update & delete employee records safely

### 📡 REST APIs (APIView)

* Employee CRUD APIs
* Custom Form APIs
* Secure responses with clear error messages
* Atomic transactions for all writes

### 📊 Dashboard

* Total employees count
* Total forms count
* Recent forms listing

---
## 🧠 Core Models

### CustomForm

* name
* description
* created_at

### FormField

* form (FK)
* label
* field_type
* order

### Employee

* form (FK)
* created_at

### EmployeeFieldValue

* employee (FK)
* field (FK)
* value

---

## 🔎 Search Logic (Employee List API)

```http
GET /api/employees/?field=Email&q=john
```

* Searches **only inside selected field label**
* Case‑insensitive matching
* Password fields are always masked

---

## 🛡 Field‑Type Validation

| Field Type | Allowed Values |
| ---------- | -------------- |
| text       | Any string     |
| number     | Digits only    |
| date       | YYYY‑MM‑DD     |
| email      | Valid email    |
| password   | Stored masked  |

Validation handled **server‑side** before save.

---

## 🔄 Transactions & Error Handling

All create/update/delete operations use:

```python
with transaction.atomic():
```
---

## 📦 Installation

```bash
git clone https://github.com/amal-dev-01/employee_management
cd employee_management
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Migrate & Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🔑 JWT Authentication

### Login

```http
POST /api/login/
```

```json
{
  "username": "admin@example.com",
  "password": "password"
}
```

### Protected API

```
Authorization: Bearer <access_token>
```

---

## 📈 Best Practices Used

* Custom User model
* APIView (explicit & maintainable)
* Clean serializers
* Atomic DB operations
* Secure password handling
* Scalable folder structure
* Separation of API & Template views

---

**Backend Developer – Django / DRF**

