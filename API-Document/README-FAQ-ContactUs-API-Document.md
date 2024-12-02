
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

---

This document provides all necessary information to test and implement the GraphQL API interactions for FAQ management and contact form submissions in your project.
