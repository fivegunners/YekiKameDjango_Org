
# GraphQL API Interaction Examples

This document provides examples of how to interact with the GraphQL API for FAQ retrieval and contact form submissions. Each example includes the request from the frontend and the expected response from the server.

---

## FAQ Operations

### Fetch All FAQs

#### Request:
```graphql
query {
    allFaqs {
        questionTitle
        questionAnswer
    }
}
```

#### Response:
```json
{
    "data": {
        "allFaqs": [
            {
                "questionTitle": "What is GraphQL?",
                "questionAnswer": "A query language for APIs."
            },
            {
                "questionTitle": "What is Django?",
                "questionAnswer": "A high-level Python web framework."
            }
        ]
    }
}
```

---

## ContactUs Operations

### Submit a Contact Form

#### Request:
```graphql
mutation {
    createContactUs(fullName: "Ali Ahmadi", email: "user@example.com", subject: "Inquiry", message: "Please contact me") {
        contact {
            fullName
            email
            subject
            message
            createdAt
        }
    }
}
```

#### Response:
```json
{
    "data": {
        "createContactUs": {
            "contact": {
                "fullName": "Ali Ahmadi",
                "email": "user@example.com",
                "subject": "Inquiry",
                "message": "Please contact me",
                "createdAt": "2024-11-29T10:00:00Z"
            }
        }
    }
}
```

## Notice Queries

### Fetch Active Notices

The `activeNotices` query allows you to fetch all active notices that have not yet expired.

#### Request:
```graphql
query {
    activeNotices {
        title
        content
    }
}
```

#### Response (if active notices exist):
```json
{
    "data": {
        "activeNotices": [
            {
                "title": "Active Notice 1",
                "content": "This is the first active notice."
            },
            {
                "title": "Active Notice 2",
                "content": "This is the second active notice."
            }
        ]
    }
}
```

#### Response (if no active notices exist):
```json
{
    "data": {
        "activeNotices": []
    }
}
```

#### Description:
- The `activeNotices` query returns an array of notices that are currently active (i.e., their `expiration_date` is greater than the current time).
- Each notice includes:
  - `title`: The title of the notice.
  - `content`: The content of the notice.

---

This document provides all necessary information to test and implement the GraphQL API interactions for FAQ management and contact form submissions in your project.
