
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


## Ticket Mutations

### Create a Ticket

The `createTicket` mutation allows you to create a new ticket.

#### Request:
```graphql
mutation {
    createTicket(
        title: "Sample Ticket",
        content: "This is the content of the ticket.",
        department: "support",
        priority: "high",
        status: "waiting",
        phone: "09123456789"
    ) {
        ticket {
            id
            title
            content
            department
            priority
            status
            createdBy {
                phone
            }
        }
    }
}
```

#### Response:
```json
{
    "data": {
        "createTicket": {
            "ticket": {
                "id": "1",
                "title": "Sample Ticket",
                "content": "This is the content of the ticket.",
                "department": "support",
                "priority": "high",
                "status": "waiting",
                "createdBy": {
                    "phone": "09123456789"
                }
            }
        }
    }
}
```

#### Description:
- `title`: The title of the ticket.
- `content`: The content or description of the ticket.
- `department`: The department the ticket is assigned to.
- `priority`: The priority level of the ticket (`low`, `medium`, `high`).
- `status`: The current status of the ticket (`waiting`, `answered`, etc.).
- `phone`: The phone number of the user creating the ticket.

---

### Create a Ticket Message

The `createTicketMessage` mutation allows you to add a new message to an existing ticket.

#### Request:
```graphql
mutation {
    createTicketMessage(
        ticketId: "1",
        phone: "09123456789",
        message: "This is a reply to the ticket."
    ) {
        ticketMessage {
            id
            message
            ticket {
                id
                title
                status
            }
            user {
                phone
            }
        }
    }
}
```

#### Response:
```json
{
    "data": {
        "createTicketMessage": {
            "ticketMessage": {
                "id": "1",
                "message": "This is a reply to the ticket.",
                "ticket": {
                    "id": "1",
                    "title": "Sample Ticket",
                    "status": "answered"
                },
                "user": {
                    "phone": "09123456789"
                }
            }
        }
    }
}
```

#### Description:
- `ticketId`: The ID of the ticket to which the message is added.
- `phone`: The phone number of the user adding the message.
- `message`: The content of the message being added.
- The response includes details about the message, the ticket it belongs to, and the user who added the message.


## Query: User Tickets

The `userTickets` query allows you to retrieve all tickets created by a user, filtered by their phone number.

### Request:
```graphql
query {
    userTickets(phone: "09123456789") {
        title
        department
        status
        priority
    }
}
```

### Responses:

#### Successful Request:
If tickets exist for the user:
```json
{
    "data": {
        "userTickets": [
            {
                "title": "Ticket 2",
                "department": "financial",
                "status": "answered",
                "priority": "medium"
            },
            {
                "title": "Ticket 1",
                "department": "technical",
                "status": "waiting",
                "priority": "high"
            }
        ]
    }
}
```

#### No Tickets Found:
If the user has not created any tickets:
```json
{
    "data": {
        "userTickets": []
    }
}
```

---

### Description:
- `phone`: The phone number of the user whose tickets are being fetched.

### Behavior:
- Returns all tickets created by the user.
- Each ticket includes the following fields:
  - `title`: The title of the ticket.
  - `department`: The department associated with the ticket.
  - `status`: The current status of the ticket (`waiting`, `answered`, etc.).
  - `priority`: The priority level of the ticket (`low`, `medium`, `high`).


## Query: Ticket Messages

The `ticketMessages` query allows you to retrieve all messages associated with a specific ticket.

### Request:
```graphql
query {
    ticketMessages(ticketId: "1") {
        id
        message
        createdAt
        user {
            phone
            fullname
            isAdmin
        }
    }
}
```

### Responses:

#### Successful Request:
If messages exist for the ticket:
```json
{
    "data": {
        "ticketMessages": [
            {
                "id": "1",
                "message": "First message",
                "createdAt": "2024-01-01T10:00:00+00:00",
                "user": {
                    "phone": "09123456789",
                    "fullname": "John Doe",
                    "isAdmin": "False"
                }
            },
            {
                "id": "2",
                "message": "Second message",
                "createdAt": "2024-01-02T12:00:00+00:00",
                "user": {
                    "phone": "09386385040",
                    "fullname": "ghost",
                    "isAdmin": "False"
                }
            }
        ]
    }
}
```

#### No Messages Found:
If the ticket does not exist or has no messages:
```json
{
    "data": {
        "ticketMessages": []
    }
}
```

---

### Description:
- `ticketId`: The ID of the ticket for which messages are being fetched.

### Behavior:
- Returns all messages associated with the specified ticket.
- Each message includes the following fields:
  - `id`: The unique identifier of the message.
  - `message`: The content of the message.
  - `createdAt`: The timestamp when the message was created.
  - `user`: Information about the user who created the message, including:
    - `phone`: The phone number of the user.
    - `fullname`: The full name of the user.

---

This document provides all necessary information to test and implement the GraphQL API interactions for FAQ management and contact form submissions in your project.
