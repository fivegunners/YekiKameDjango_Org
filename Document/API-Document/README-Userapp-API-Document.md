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
### Update Email

The `updateEmail` mutation allows a user to update their email address.

#### Request:
```graphql
mutation {
    updateEmail(phone: "09123456789", email: "newemail@example.com") {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updateEmail": {
            "success": true,
            "message": "Email updated successfully."
        }
    }
}
```

#### Description:
- `phone`: The phone number of the user.
- `email`: The new email address to be set for the user.

---

### Update Fullname

The `updateFullname` mutation allows a user to update their full name.

#### Request:
```graphql
mutation {
    updateFullname(phone: "09123456789", fullname: "John Doe") {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updateFullname": {
            "success": true,
            "message": "Fullname updated successfully."
        }
    }
}
```

#### Description:
- `phone`: The phone number of the user.
- `fullname`: The new full name to be set for the user.

---

### Update Password

The `updatePassword` mutation allows a user to update their password.

#### Request:
```graphql
mutation {
    updatePassword(phone: "09123456789", oldPassword: "oldpassword", newPassword: "newpassword123") {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updatePassword": {
            "success": true,
            "message": "Password updated successfully."
        }
    }
}
```

#### Description:
- `phone`: The phone number of the user.
- `oldPassword`: The current password of the user.
- `newPassword`: The new password to be set for the user.

#### Error Response (Incorrect Old Password):
```json
{
    "data": {
        "updatePassword": {
            "success": false,
            "message": "Old password is incorrect."
        }
    }
}
```

#### Error Response (User Not Found):
```json
{
    "data": {
        "updatePassword": {
            "success": false,
            "message": "User not found."
        }
    }
}
```


## Query: Fetch User Details

The `user` query allows you to fetch details of a user by providing their phone number.

### Request:
```graphql
query {
    user(phone: "09123456789") {
        id
        phone
        email
        fullname
        isActive
        isAdmin
    }
}
```

### Response (If User Exists):
```json
{
    "data": {
        "user": {
            "id": "1",
            "phone": "09123456789",
            "email": "example@example.com",
            "fullname": "John Doe",
            "isActive": true,
            "isAdmin": false
        }
    }
}
```

### Response (If User Does Not Exist):
```json
{
    "data": {
        "user": null
    }
}
```

### Description:
- `phone`: The phone number of the user to fetch.
- The response includes:
  - `id`: The unique identifier of the user.
  - `phone`: The user's phone number.
  - `email`: The user's email address.
  - `fullname`: The full name of the user.
  - `isActive`: Indicates whether the user's account is active.
  - `isAdmin`: Indicates whether the user has admin privileges.

---

This document provides all necessary information to test and implement the GraphQL API interactions for user authentication in your project.