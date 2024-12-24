
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
        title: "Event in Tehran",
        eventCategory: "education",
        aboutEvent: "This is a detailed description of the event.",
        startDate: "2024-12-22T10:00:00+00:00",
        endDate: "2024-12-22T18:00:00+00:00",
        province: "تهران",
        city: "تهران",
        neighborhood: "تهرانپارس",
        postalAddress: "تهرانپارس، خیابان ۱۷۴ غربی",
        postalCode: "1592634780",
        registrationStartDate: "2024-12-20T10:00:00+00:00",
        registrationEndDate: "2024-12-21T18:00:00+00:00",
        fullDescription: "This is the full description of the event.",
        maxSubscribers: 100,
        eventOwnerPhone: "09123456789"
    ) {
        event {
            id
            title
            eventCategory
            city
            startDate
            neighborhood
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
                "id": 1,
                "title": "Event in Tehran",
                "eventCategory": "education",
                "city": "تهران",
                "neighborhood": "تهرانپارس",
                "startDate": "2024-12-22T10:00:00+00:00",
                "maxSubscribers": 100
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

## Review and Comment Queries

### Fetch Reviews by Event

#### Request:
```graphql
query {
    reviewsByEvent(eventId: "1") {
        id
        rating
        commentText
        createdAt
    }
}
```

#### Response:
```json
{
    "data": {
        "reviewsByEvent": [
            {
                "id": "3",
                "rating": 5.0,
                "commentText": "Absolutely loved it!",
                "createdAt": "2024-12-21T15:30:00+00:00"
            },
            {
                "id": "2",
                "rating": 4.5,
                "commentText": "Great event!",
                "createdAt": "2024-12-20T10:30:00+00:00"
            },
            {
                "id": "1",
                "rating": 3.0,
                "commentText": "It was okay.",
                "createdAt": "2024-12-19T09:00:00+00:00"
            }
        ]
    }
}
```

### Fetch Comments by Review

#### Request:
```graphql
query {
    commentsByReview(reviewId: "1") {
        id
        commentText
        createdAt
        level
        isActive
    }
}
```

#### Response:
```json
{
    "data": {
        "commentsByReview": [
            {
                "id": "3",
                "commentText": "Not great.",
                "createdAt": "2024-12-21T16:00:00+00:00",
                "level": 1,
                "isActive": true
            },
            {
                "id": "2",
                "commentText": "It was okay.",
                "createdAt": "2024-12-21T14:00:00+00:00",
                "level": 1,
                "isActive": true
            },
            {
                "id": "1",
                "commentText": "Loved it!",
                "createdAt": "2024-12-21T12:00:00+00:00",
                "level": 1,
                "isActive": true
            }
        ]
    }
}
```

## Event Queries

### Fetch Event Details

The `eventDetails` query allows you to fetch all the details of a specific event by its ID.

#### Request:
```graphql
query {
    eventDetails(eventId: "1") {
        event {
            id
            title
            eventCategory
            aboutEvent
            startDate
            endDate
            province
            city
            neighborhood
            postalAddress
            postalCode
            registrationStartDate
            registrationEndDate
            fullDescription
            maxSubscribers
            eventOwner {
                phone
            }
        }
        error
    }
}
```

#### Response (if event exists):
```json
{
    "data": {
        "eventDetails": {
            "event": {
                "id": "1",
                "title": "Event in Tehran",
                "eventCategory": "education",
                "aboutEvent": "This is a detailed description of the event.",
                "startDate": "2024-12-22T10:00:00+00:00",
                "endDate": "2024-12-22T18:00:00+00:00",
                "province": "تهران",
                "city": "تهران",
                "neighborhood": "تهرانپارس",
                "postalAddress": "تهرانپارس، خیابان ۱۷۴ غربی",
                "postalCode": "1592634780",
                "registrationStartDate": "2024-12-20T10:00:00+00:00",
                "registrationEndDate": "2024-12-21T18:00:00+00:00",
                "fullDescription": "This is the full description of the event.",
                "maxSubscribers": 100,
                "eventOwner": {
                    "phone": "09123456789"
                }
            },
            "error": null
        }
    }
}
```

#### Response (if event does not exist):
```json
{
    "data": {
        "eventDetails": {
            "event": null,
            "error": "Event does not exist!"
        }
    }
}
```

#### Description:
- `eventId`: The ID of the event to fetch details for.
- The response includes all fields related to the event, such as its `title`, `eventCategory`, `startDate`, `endDate`, `province`, `city`, `neighborhood`, and more.
- If the event does not exist, the `event` field will be `null`, and the `error` field will contain an appropriate message.

### Fetch Related Events

The `relatedEvents` query allows you to fetch up to 5 events that share the same category as a given event.

#### Request:
```graphql
query {
    relatedEvents(eventId: "1") {
        title
        eventCategory
    }
}
```

#### Response (if related events exist):
```json
{
    "data": {
        "relatedEvents": [
            {
                "title": "Related Event 1",
                "eventCategory": "education"
            },
            {
                "title": "Related Event 2",
                "eventCategory": "education"
            },
            {
                "title": "Related Event 3",
                "eventCategory": "education"
            },
            {
                "title": "Related Event 4",
                "eventCategory": "education"
            },
            {
                "title": "Related Event 5",
                "eventCategory": "education"
            }
        ]
    }
}
```

#### Response (if no related events exist):
```json
{
    "data": {
        "relatedEvents": []
    }
}
```

#### Description:
- `eventId`: The ID of the event to fetch related events for.
- The response includes up to 5 related events that have the same category (`eventCategory`) as the given event.
- Each related event includes:
  - `title`: The title of the related event.
  - `eventCategory`: The category of the related event.

---

This document provides the necessary information to test and implement the GraphQL API interactions for event management in your project.
