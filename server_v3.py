from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("  TAXSEE MOCK SERVER v3 - Professional Edition")
    print("=" * 60)
    print("  Database: SQLite (persistent)")
    print("  Auth: HMAC signed token")
    print("  Rate limit: 5 request/menit")
    print("=" * 60)
    print("  Endpoints:")
    print("    POST /api/v1/login")
    print("    GET  /api/v1/shifts")
    print("    POST /api/v1/shift/{id}/buy")
    print("    POST /api/v1/shift/{id}/activate")
    print("    GET  /api/v1/balance")
    print("    POST /api/v1/topup")
    print("    GET  /api/v1/transactions")
    print("    POST /admin/seed")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5009, debug=False)
