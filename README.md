# Taxsee Mock Server v3

REST API profesional untuk simulasi platform driver. Dibuat untuk pembelajaran backend security & API design.

## Fitur

- Database SQLite (persistent)
- Auth HMAC (signed token)
- Rate Limiting (5 request/menit)
- Server-side Validation
- Transaction Logging
- Modular Structure
- Seed Data untuk testing

## Teknologi

- Python 3.14
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- SQLite 3
- HMAC SHA-256

## Arsitektur

taxsee-mock/
- app/models/ - Database models
- app/routes/ - API endpoints
- app/middleware/ - Auth, rate limiting
- app/utils/ - Helper functions
- tests/ - Unit tests
- docs/ - API documentation
- data/ - SQLite database
- server_v3.py - Entry point

## Endpoints

### Auth
- POST /api/v1/login

### Shifts
- GET /api/v1/shifts
- POST /api/v1/shift/{id}/buy
- POST /api/v1/shift/{id}/activate

### Balance
- GET /api/v1/balance
- POST /api/v1/topup
- GET /api/v1/transactions

### Admin
- POST /admin/seed
- GET /admin/users

## Cara Jalankan

pip install -r requirements.txt
python server_v3.py

## Security Features

1. Server-side Validation
2. HMAC Signature
3. Rate Limiting
4. Server-side Record

## Author

[Nama Kamu]
