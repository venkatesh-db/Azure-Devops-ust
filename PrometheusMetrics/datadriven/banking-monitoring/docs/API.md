# API Documentation - Banking Application

## Overview
RESTful API for banking operations with full monitoring and logging integration.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required for demo. In production, implement:
- JWT tokens
- OAuth2
- Azure AD

## Endpoints

### Health & Status

#### GET /health
Check application health and statistics
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-19T10:30:45.123456",
  "accounts_count": 5,
  "transactions_count": 12
}
```

### Account Management

#### POST /accounts
Create a new bank account
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_holder": "John Doe",
    "initial_balance": 5000,
    "account_type": "checking"
  }'
```

**Request Body:**
```json
{
  "account_holder": "string (required)",
  "initial_balance": "number (required, >= 0)",
  "account_type": "string (optional: 'savings', 'checking', 'money_market')"
}
```

**Response:** 201 Created
```json
{
  "account_id": "ACC-a1b2c3d4e5f6",
  "account_holder": "John Doe",
  "balance": 5000,
  "account_type": "checking",
  "is_active": true,
  "created_at": "2024-01-19T10:30:45.123456"
}
```

**Tracked Metrics:**
- `account_created` event
- `accounts_total` gauge updated

---

#### GET /accounts/{account_id}
Retrieve account details
```bash
curl http://localhost:5000/api/accounts/ACC-a1b2c3d4e5f6
```

**Response:** 200 OK
```json
{
  "account_id": "ACC-a1b2c3d4e5f6",
  "account_holder": "John Doe",
  "balance": 4500,
  "account_type": "checking",
  "is_active": true,
  "created_at": "2024-01-19T10:30:45.123456"
}
```

**Tracked Metrics:**
- `get_account` operation duration
- API request count & latency

---

#### GET /accounts/{account_id}/balance
Get current account balance
```bash
curl http://localhost:5000/api/accounts/ACC-a1b2c3d4e5f6/balance
```

**Response:** 200 OK
```json
{
  "account_id": "ACC-a1b2c3d4e5f6",
  "balance": 4500,
  "currency": "USD",
  "timestamp": "2024-01-19T10:30:45.123456"
}
```

### Transactions

#### POST /transactions/transfer
Transfer funds between accounts
```bash
curl -X POST http://localhost:5000/api/transactions/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "ACC-a1b2c3d4e5f6",
    "to_account": "ACC-x9y8z7w6v5u4",
    "amount": 500,
    "description": "Payment for services"
  }'
```

**Request Body:**
```json
{
  "from_account": "string (required)",
  "to_account": "string (required)",
  "amount": "number (required, > 0)",
  "description": "string (optional)"
}
```

**Response:** 200 OK
```json
{
  "transaction_id": "TXN-550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "timestamp": "2024-01-19T10:30:45.123456"
}
```

**Errors:**
- 400: Invalid amount, insufficient balance, same account
- 400: Account not found

**Tracked Metrics:**
- `transfer_completed` event with amounts
- Transaction latency histogram
- `transfer_funds` operation count
- Account balances updated

---

#### POST /transactions/deposit
Deposit funds to an account
```bash
curl -X POST http://localhost:5000/api/transactions/deposit \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "ACC-a1b2c3d4e5f6",
    "amount": 1000,
    "description": "Salary deposit"
  }'
```

**Request Body:**
```json
{
  "account_id": "string (required)",
  "amount": "number (required, > 0)",
  "description": "string (optional)"
}
```

**Response:** 200 OK
```json
{
  "transaction_id": "TXN-550e8400-e29b-41d4-a716-446655440000",
  "status": "completed"
}
```

**Tracked Metrics:**
- `deposit_completed` event
- Account balance updated
- Transaction recorded

---

#### GET /transactions/{transaction_id}
Retrieve specific transaction details
```bash
curl http://localhost:5000/api/transactions/TXN-550e8400-e29b-41d4-a716-446655440000
```

**Response:** 200 OK
```json
{
  "transaction_id": "TXN-550e8400-e29b-41d4-a716-446655440000",
  "from_account": "ACC-a1b2c3d4e5f6",
  "to_account": "ACC-x9y8z7w6v5u4",
  "amount": 500,
  "type": "transfer",
  "description": "Payment for services",
  "timestamp": "2024-01-19T10:30:45.123456",
  "status": "completed",
  "details": {}
}
```

---

#### GET /transactions
List transactions with filtering
```bash
# All transactions, latest 50
curl http://localhost:5000/api/transactions

# For specific account
curl http://localhost:5000/api/transactions?account_id=ACC-a1b2c3d4e5f6&limit=100
```

**Query Parameters:**
- `account_id` (string, optional): Filter by account
- `limit` (number, optional, default=100): Max results

**Response:** 200 OK
```json
{
  "total": 12,
  "transactions": [
    {
      "transaction_id": "TXN-...",
      "from_account": "ACC-...",
      "to_account": "ACC-...",
      "amount": 500,
      "type": "transfer",
      "timestamp": "2024-01-19T10:30:45.123456",
      "status": "completed"
    }
  ]
}
```

## Error Handling

### Error Response Format
```json
{
  "error": "Description of the error"
}
```

### Common Error Codes

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Missing required fields | Request validation failed |
| 400 | Account not found | Account ID doesn't exist |
| 400 | Insufficient balance | Not enough funds |
| 400 | Cannot transfer to same account | Invalid transfer |
| 500 | Internal server error | Unhandled exception |

## Monitoring Headers

Add custom headers for better monitoring:

```bash
curl -H "X-User-ID: user123" \
     -H "X-Request-ID: req456" \
     http://localhost:5000/api/accounts
```

These headers are:
- Logged in Application Insights
- Available in trace metadata
- Used for user activity tracking

## Performance Characteristics

### Typical Response Times
- GET /accounts: 10-50ms
- POST /accounts: 50-200ms
- POST /transactions/transfer: 100-500ms
- GET /transactions: 50-100ms (depends on limit)

### Rate Limits
Currently unlimited. In production, implement:
- Per-user rate limiting
- IP-based throttling
- Token bucket algorithm

## Examples

### Complete Transaction Flow
```bash
# 1. Create first account
ACC1=$(curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"account_holder": "Alice", "initial_balance": 5000}' \
  | jq -r '.account_id')

# 2. Create second account
ACC2=$(curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"account_holder": "Bob", "initial_balance": 3000}' \
  | jq -r '.account_id')

# 3. Transfer funds
TXN=$(curl -X POST http://localhost:5000/api/transactions/transfer \
  -H "Content-Type: application/json" \
  -d "{
    \"from_account\": \"$ACC1\",
    \"to_account\": \"$ACC2\",
    \"amount\": 500
  }" | jq -r '.transaction_id')

# 4. View transaction details
curl http://localhost:5000/api/transactions/$TXN | jq .

# 5. Check balances
curl http://localhost:5000/api/accounts/$ACC1/balance | jq .
curl http://localhost:5000/api/accounts/$ACC2/balance | jq .
```

### Deposit and Check Balance
```bash
# Deposit
curl -X POST http://localhost:5000/api/transactions/deposit \
  -H "Content-Type: application/json" \
  -d "{
    \"account_id\": \"$ACC1\",
    \"amount\": 2000
  }"

# Check new balance
curl http://localhost:5000/api/accounts/$ACC1/balance | jq '.'
```

## Integration with Monitoring

### Application Insights Events
All operations generate events:
- `account_created`: New account
- `transfer_completed`: Successful transfer
- `deposit_completed`: Successful deposit
- `transfer_failed`: Failed transfer attempt
- `validation_error`: Invalid request

### Prometheus Metrics
- `banking_transactions_total{type, status}`: Transaction count
- `banking_transaction_amount_total{type}`: Total amounts
- `banking_transaction_duration_seconds{type}`: Processing time
- `banking_accounts_total{account_type}`: Account count
- `banking_api_requests_total{method, endpoint, status}`: API metrics
- `banking_api_request_duration_seconds{method, endpoint}`: API latency

### Log Entries
Each request generates log entry with:
- Timestamp
- Operation name
- Duration
- Status (success/failure)
- User ID
- Custom dimensions

## Versioning

Current version: v1
- No versioning in URLs currently
- All endpoints use consistent naming

Future versions will use URL paths:
- `/api/v1/accounts`
- `/api/v2/accounts`
