# GraphQL API Interaction Examples

This document provides examples of how to interact with the GraphQL API for user authentication operations including signup, login, and OTP verification. Each example includes the request from the frontend and the expected response from the server.

---

## Signup User

### Request:
```graphql
mutation {
    registerUser(phone: "09120000000", password: "mypassword123") {
        success
    }
}
```

### Response:
```json
{
    "data": {
        "registerUser": {
            "success": true
        }
    }
}
```

---

## Verify Signup OTP

### Request:
```graphql
mutation {
    verifyOtp(phone: "09120000000", otp: 12345) {
        success
        token
    }
}
```

### Response:
#### If OTP is correct:
```json
{
    "data": {
        "verifyOtp": {
            "success": true,
            "token": "<session_token>"
        }
    }
}
```

#### If OTP is incorrect:
```json
{
    "data": {
        "verifyOtp": {
            "success": false,
            "token": null
        }
    }
}
```

---

## Login with Password

### Request:
```graphql
mutation {
    loginUser(phone: "09120000000", password: "mypassword123") {
        success
        token
    }
}
```

### Response:
#### If credentials are correct:
```json
{
    "data": {
        "loginUser": {
            "success": true,
            "token": "<session_token>"
        }
    }
}
```

#### If credentials are incorrect:
```json
{
    "data": {
        "loginUser": {
            "success": false,
            "token": null
        }
    }
}
```

---

## Request Login OTP

### Request:
```graphql
mutation {
    requestLoginOtp(phone: "09120000000") {
        success
    }
}
```

### Response:
#### If request is successful:
```json
{
    "data": {
        "requestLoginOtp": {
            "success": true
        }
    }
}
```

---

## Verify Login OTP

### Request:
```graphql
mutation {
    verifyLoginOtp(phone: "09120000000", otp: 54321) {
        success
        token
    }
}
```

### Response:
#### If OTP is correct:
```json
{
    "data": {
        "verifyLoginOtp": {
            "success": true,
            "token": "<session_token>"
        }
    }
}
```

#### If OTP is incorrect:
```json
{
    "data": {
        "verifyLoginOtp": {
            "success": false,
            "token": null
        }
    }
}
```

---

This document provides all necessary information to test and implement the GraphQL API interactions for user authentication in your project.