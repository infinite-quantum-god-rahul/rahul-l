# SML87 Django REST API Documentation

## Overview
This document describes the REST API endpoints available for the SML87 Django backend, designed to work with Flutter mobile applications.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. All endpoints require authentication except where noted.

### Login
```
POST /api/auth/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Refresh Token
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### Authorization Header
Include the JWT token in all authenticated requests:
```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### 1. Authentication & User Management

#### Get User Profile
```
GET /api/user/profile/
Authorization: Bearer <token>
```

#### Response
```json
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": true,
    "is_superuser": false,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z",
    "role_flags": {
        "admin": false,
        "master": true,
        "data_entry": false,
        "accounting": false,
        "recovery_agent": false,
        "auditor": false,
        "manager": false
    }
}
```

### 2. Dashboard & Statistics

#### Get Dashboard Stats
```
GET /api/dashboard/stats/
Authorization: Bearer <token>
```

#### Response
```json
{
    "total_clients": 150,
    "total_loans": 89,
    "total_disbursed": 2500000.00,
    "total_collected": 1800000.00,
    "total_npa": 150000.00,
    "active_field_schedules": 25,
    "pending_kyc": 12,
    "overdue_loans": 8
}
```

### 3. Search Functionality

#### Search Across Entities
```
GET /api/search/?query=john&entity_type=clients&limit=10
Authorization: Bearer <token>
```

#### Parameters
- `query` (required): Search term
- `entity_type` (optional): Specific entity type (clients, loans, field_schedules)
- `limit` (optional): Maximum results (default: 20)

#### Response
```json
{
    "clients": [
        {
            "id": 1,
            "code": "CL001",
            "name": "John Doe",
            "mobile": "9876543210",
            "photo_url": "http://127.0.0.1:8000/media/photos/john.jpg"
        }
    ],
    "loans": [...],
    "field_schedules": [...]
}
```

### 4. Client Management

#### Get All Clients
```
GET /api/clients/
Authorization: Bearer <token>
```

#### Get Client by ID
```
GET /api/clients/{id}/
Authorization: Bearer <token>
```

#### Create Client
```
POST /api/clients/
Authorization: Bearer <token>
Content-Type: application/json

{
    "code": "CL002",
    "name": "Jane Smith",
    "mobile": "9876543211"
}
```

#### Update Client
```
PUT /api/clients/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Jane Smith Updated",
    "mobile": "9876543211"
}
```

#### Delete Client
```
DELETE /api/clients/{id}/
Authorization: Bearer <token>
```

#### Upload Client Photo
```
POST /api/clients/{id}/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

photo: [file]
```

### 5. Loan Management

#### Get All Loan Applications
```
GET /api/loan-applications/
Authorization: Bearer <token>
```

#### Get Loans by Status
```
GET /api/loan-applications/by_status/?status=pending
Authorization: Bearer <token>
```

#### Get Loans by Client
```
GET /api/loan-applications/by_client/?client_id=1
Authorization: Bearer <token>
```

#### Create Loan Application
```
POST /api/loan-applications/
Authorization: Bearer <token>
Content-Type: application/json

{
    "application_id": "LA001",
    "client": 1,
    "loan_type": "personal",
    "loan_amount": 50000.00,
    "tenure_months": 24,
    "interest_rate": 12.5,
    "status": "pending"
}
```

### 6. Field Operations

#### Get All Field Schedules
```
GET /api/field-schedules/
Authorization: Bearer <token>
```

#### Get Active Field Schedules
```
GET /api/field-schedules/active/
Authorization: Bearer <token>
```

#### Get Schedules by Staff
```
GET /api/field-schedules/by_staff/?staff_id=1
Authorization: Bearer <token>
```

#### Create Field Schedule
```
POST /api/field-schedules/
Authorization: Bearer <token>
Content-Type: application/json

{
    "reference_number": "FS001",
    "staff": 1,
    "village": "Village A",
    "scheduled_date": "2024-01-15",
    "purpose": "Loan verification",
    "status": "active"
}
```

#### Get Field Visits
```
GET /api/field-visits/
Authorization: Bearer <token>
```

#### Get Visits by Schedule
```
GET /api/field-visits/by_schedule/?schedule_id=1
Authorization: Bearer <token>
```

### 7. NPA Management

#### Get All NPA Accounts
```
GET /api/npa-accounts/
Authorization: Bearer <token>
```

#### Get NPA by Status
```
GET /api/npa-accounts/by_status/?status=active
Authorization: Bearer <token>
```

### 8. KYC Management

#### Get All KYC Documents
```
GET /api/kyc-documents/
Authorization: Bearer <token>
```

#### Get Pending KYC
```
GET /api/kyc-documents/pending/
Authorization: Bearer <token>
```

#### Upload KYC Document
```
POST /api/kyc-documents/{id}/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

document: [file]
```

### 9. Financial Management

#### Get Account Heads
```
GET /api/account-heads/
Authorization: Bearer <token>
```

#### Get Vouchers
```
GET /api/vouchers/
Authorization: Bearer <token>
```

#### Get Postings
```
GET /api/postings/
Authorization: Bearer <token>
```

#### Get Payments
```
GET /api/payments/
Authorization: Bearer <token>
```

#### Get Repayments
```
GET /api/repayments/
Authorization: Bearer <token>
```

### 10. Company & Branch Management

#### Get All Companies
```
GET /api/companies/
Authorization: Bearer <token>
```

#### Get All Staff
```
GET /api/staff/
Authorization: Bearer <token>
```

## File Upload Endpoints

### Generic File Upload
```
POST /api/upload/{entity}/{pk}/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: [file]
```

### Supported Entity Types
- clients
- staff
- companies
- field-schedules
- kyc-documents

## Error Handling

### Standard Error Response
```json
{
    "detail": "Error message description"
}
```

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Pagination

Most list endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)

### Paginated Response
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/clients/?page=2",
    "previous": null,
    "results": [...]
}
```

## Filtering & Sorting

### Filtering
Most endpoints support filtering by model fields:
```
GET /api/clients/?status=active&branch=1
```

### Sorting
Sort by specific fields:
```
GET /api/loan-applications/?ordering=-created_at
GET /api/clients/?ordering=name
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- Authentication endpoints: 5 requests per minute
- Other endpoints: 100 requests per minute

## CORS Configuration

CORS is enabled for development. For production, configure allowed origins in Django settings.

## Testing the API

### Using curl
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Get clients with token
curl -X GET http://127.0.0.1:8000/api/clients/ \
  -H "Authorization: Bearer <your_token>"
```

### Using Postman
1. Import the collection
2. Set the base URL to `http://127.0.0.1:8000/api/`
3. Use the login endpoint to get a token
4. Set the Authorization header with the token for other requests

## Flutter Integration Example

```dart
class SMLApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/';
  static String? _token;

  static Future<void> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('${baseUrl}auth/token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _token = data['access'];
    }
  }

  static Future<List<Client>> getClients() async {
    final response = await http.get(
      Uri.parse('${baseUrl}clients/'),
      headers: {'Authorization': 'Bearer $_token'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return (data['results'] as List)
          .map((json) => Client.fromJson(json))
          .toList();
    }
    return [];
  }

  static Future<Map<String, dynamic>> getDashboardStats() async {
    final response = await http.get(
      Uri.parse('${baseUrl}dashboard/stats/'),
      headers: {'Authorization': 'Bearer $_token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return {};
  }
}
```

## Support & Contact

For API support or questions, contact the development team or refer to the Django backend logs for debugging information.

