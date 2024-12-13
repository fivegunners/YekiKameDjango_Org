
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
        city
        postalAddress
        postalCode
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
                "city": "تهران",
                "postalAddress": "تهرانپارس، خیابان ۱۷۴ غربی",
                "postalCode": "1592634780"
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
        neighborhood
        postalAddress
        postalCode
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
                "postalAddress": "شیراز، بلوار حافظ",
                "postalCode": "2631598470"
            },
            {
                "id": 2,
                "title": "Event in Mashhad",
                "eventCategory": "sport",
                "subscriberCount": 50,
                "neighborhood": "خیابان امام رضا (ع)",
                "postalAddress": "مشهد، خیابان امام رضا (ع)",
                "postalCode": "4871592630"
            },
            {
                "id": 3,
                "title": "Event in Tehran",
                "eventCategory": "education",
                "subscriberCount": 100,
                "neighborhood": "تهرانپارس",
                "postalAddress": "تهرانپارس، خیابان ۱۷۴ غربی",
                "postalCode": "1592634780"
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

---

This document provides the necessary information to test and implement the GraphQL API interactions for event management in your project.
