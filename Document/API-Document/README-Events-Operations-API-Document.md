
# GraphQL API Interaction Examples for Event Operations

This document provides examples of how to interact with the GraphQL API for event management operations, including searching events by city, fetching recent events, and creating new events.

---

## Event Queries

### Search Events by City

#### Request:
```graphql
query {
    searchEventsByCity(city: "تهران") {
        id
        title
        eventCategory
        subscriberCount
        startDate
        neighborhood
    }
}
```

#### Response:
```json
{
    "data": {
        "searchEventsByCity": [
            {
                "id": 5,
                "title": "Event in Tehran",
                "eventCategory": "education",
                "neighborhood": "تهرانپارس",
                "subscriberCount": 20,
                "startDate": "2024-12-01T09:00:00+00"
            }
        ]
    }
}
```

### Fetch Recent Events

#### Request:
```graphql
query {
    recentEvents {
        id
        title
        eventCategory
        subscriberCount
        startDate
        neighborhood
    }
}
```

#### Response:
```json
{
    "data": {
        "recentEvents": [
            {
                "id": 1,
                "title": "Event in Shiraz",
                "eventCategory": "game",
                "subscriberCount": 80,
                "neighborhood": "بلوار حافظ",
                "startDate": "2024-12-01T09:00:00+00"
            },
            {
                "id": 2,
                "title": "Event in Mashhad",
                "eventCategory": "sport",
                "subscriberCount": 50,
                "neighborhood": "خیابان امام رضا (ع)",
                "startDate": "2024-12-01T09:00:00+00"
            },
            {
                "id": 3,
                "title": "Event in Tehran",
                "eventCategory": "education",
                "neighborhood": "تهرانپارس",
                "subscriberCount": 20,
                "startDate": "2024-12-01T09:00:00+00"
            }
        ]
    }
}
```

---

## Event Mutation

### Create a New Event

#### Request:
```graphql
mutation {
    createEvent(
        title: "New Event",
        eventCategory: "entertainment",
        aboutEvent: "A new entertainment event.",
        startDate: "2024-12-01T09:00:00Z",
        endDate: "2024-12-01T17:00:00Z",
        registrationStartDate: "2024-11-01T09:00:00Z",
        registrationEndDate: "2024-11-25T17:00:00Z",
        province: "تهران",
        city: "تهران",
        neighborhood: "District 1",
        postalAddress: "Some Street, Tehran",
        postalCode: "1234567890",
        maxSubscribers: 150,
        eventOwnerPhone: "09123456789"
    ) {
        event {
            title
            eventCategory
            neighborhood
            postalAddress
            postalCode
            maxSubscribers
        }
    }
}
```

#### Response:
```json
{
    "data": {
        "createEvent": {
            "event": {
                "title": "New Event",
                "eventCategory": "entertainment",
                "neighborhood": "District 1",
                "postalAddress": "Some Street, Tehran",
                "postalCode": "1234567890",
                "maxSubscribers": 150
            }
        }
    }
}
```

## Review and Comment Mutations

### CreateReview Mutation

The `CreateReview` mutation allows users to create a review for an event. The review includes a rating and a comment text.

#### Request:
```graphql
mutation {
  createReview(eventId: "1", userId: "1", rating: 4.5, commentText: "This is a great event!") {
    review {
      id
      rating
      commentText
    }
  }
}
```

#### Response:
```json
{
  "data": {
    "createReview": {
      "review": {
        "id": 1,
        "rating": 4.5,
        "commentText": "This is a great event!"
      }
    }
  }
}
```

#### Description:
- `eventId`: The ID of the event for which the review is being created.
- `userId`: The ID of the user submitting the review.
- `rating`: A floating-point value representing the rating (from 0 to 5).
- `commentText`: The text content of the review.

---

### CreateComment Mutation

The `CreateComment` mutation allows users to create a comment for a specific review. It supports replying to existing comments, and the `level` field keeps track of comment replies (with a limit of 3 levels).

#### Request:
```graphql
mutation {
  createComment(reviewId: "1", userId: "1", commentText: "I agree with this review!", isActive: true) {
    comment {
      id
      commentText
      isActive
      level
    }
  }
}
```

#### Response:
```json
{
  "data": {
    "createComment": {
      "comment": {
        "id": 1,
        "commentText": "I agree with this review!",
        "isActive": true,
        "level": 1
      }
    }
  }
}
```

#### Description:
- `reviewId`: The ID of the review to which the comment is being added.
- `userId`: The ID of the user submitting the comment.
- `commentText`: The text content of the comment.
- `isActive`: Indicates whether the comment is active.
- `level`: The level of the comment (for replies to comments, this increases). The level is restricted to a maximum of 3.

---

This document provides the necessary information to test and implement the GraphQL API interactions for event management in your project.
