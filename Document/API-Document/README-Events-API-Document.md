
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
        image
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
                "startDate": "2024-12-01T09:00:00+00",
                "image": "event_images/event1.jpg"
            },
            {
                "id": 2,
                "title": "Event in Mashhad",
                "eventCategory": "sport",
                "subscriberCount": 50,
                "neighborhood": "خیابان امام رضا (ع)",
                "startDate": "2024-12-01T09:00:00+00",
                "image": null
            },
            {
                "id": 3,
                "title": "Event in Tehran",
                "eventCategory": "education",
                "neighborhood": "تهرانپارس",
                "subscriberCount": 20,
                "startDate": "2024-12-01T09:00:00+00",
                "image": "event_images/event3.jpg"
            }
        ]
    }
}
```

---

## Event Mutation

### Create a New Event

The `createEvent` mutation allows you to create a new event with all its details, including the option to upload an image.

---

#### Request:
```graphql
mutation ($image: Upload!) {
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
        eventOwnerPhone: "09123456789",
        image: $image
    ) {
        event {
            id
            title
            eventCategory
            city
            startDate
            neighborhood
            maxSubscribers
            image
        }
    }
}
```

---

#### Variables:
```json
{
    "image": null
}
```

---

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
                "maxSubscribers": 100,
                "image": "event_images/example.jpg"
            }
        }
    }
}
```

---

#### Description:
- **Required Fields:**
  - `title`: The title of the event.
  - `eventCategory`: The category of the event (`education`, `sport`, etc.).
  - `aboutEvent`: A brief description of the event.
  - `startDate` and `endDate`: The start and end dates/times of the event.
  - `province` and `city`: The location of the event.
  - `registrationStartDate` and `registrationEndDate`: The registration period for the event.
  - `maxSubscribers`: The maximum number of participants.
  - `eventOwnerPhone`: The phone number of the event owner.
- **Optional Fields:**
  - `neighborhood`: The neighborhood where the event takes place.
  - `postalAddress` and `postalCode`: The address and postal code of the event location.
  - `image`: An image representing the event, uploaded via the `Upload` scalar.

#### Behavior:
- Validates that `endDate > startDate` and `registrationEndDate > registrationStartDate`.
- Stores the uploaded image in the `event_images/` directory.
- Returns the created event details, including the `id`, `title`, and `image` path if provided.


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
            image
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
                "image": "event_images/event1.jpg",
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
        id
        title
        eventCategory
        subscriberCount
        startDate
        neighborhood
        image
    }
}
```

#### Response (if related events exist):
```json
{
    "data": {
        "relatedEvents": [
            {
                "id": 1,
                "title": "Related Event 1",
                "eventCategory": "education",
                "subscriberCount": 50,
                "startDate": "2024-12-22T10:00:00+00:00",
                "neighborhood": "تهرانپارس",
                "image": "event_images/event1.jpg"
            },
            {
                "id": 4,
                "title": "Related Event 2",
                "eventCategory": "education",
                "subscriberCount": 100,
                "startDate": "2024-08-22T10:00:00+00:00",
                "neighborhood": "خاک سفید",
                "image": "event_images/event4.jpg"
            },
            {
                "id": 6,
                "title": "Related Event 3",
                "eventCategory": "education",
                "subscriberCount": 94,
                "startDate": "2024-09-22T10:00:00+00:00",
                "neighborhood": "گیشا",
                "image": "event_images/event6.jpg"
            },
            {
                "id": 98,
                "title": "Related Event 4",
                "eventCategory": "education",
                "subscriberCount": 15,
                "startDate": "2024-16-22T10:00:00+00:00",
                "neighborhood": "دربند",
                "image": "event_images/event98.jpg"
            },
            {
                "id": 45,
                "title": "Related Event 5",
                "eventCategory": "education",
                "subscriberCount": 75,
                "startDate": "2024-13-22T10:00:00+00:00",
                "neighborhood": "نارمک",
                "image": "event_images/event45.jpg"
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


## Mutation: Update Event Detail

The `updateEventDetail` mutation allows the owner or an admin of an event to update its details.

### Role-Based Permissions:
- **Owner**: Can update all fields of the event.
- **Admin**: Can only update the following fields:
  - `about_event`
  - `image`
  - `start_date`
  - `end_date`
  - `registration_start_date`
  - `registration_end_date`
  - `full_description`
  - `max_subscribers`

---

### Request (By Owner):
```graphql
mutation {
    updateEventDetail(
        eventId: "1",
        phone: "09123456789",
        title: "Updated Event Title",
        aboutEvent: "Updated description",
        startDate: "2024-01-02T10:00:00+00:00"
    ) {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updateEventDetail": {
            "success": true,
            "message": "Event updated successfully by the owner."
        }
    }
}
```

---

### Request (By Admin):
```graphql
mutation {
    updateEventDetail(
        eventId: "1",
        phone: "09123456788",
        aboutEvent: "Admin updated description",
        startDate: "2024-01-03T10:00:00+00:00",
        image: "event_images/event1.jpg"
    ) {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updateEventDetail": {
            "success": true,
            "message": "Event updated successfully by the admin."
        }
    }
}
```

---

### Request (Unauthorized User):
```graphql
mutation {
    updateEventDetail(
        eventId: "1",
        phone: "09123456787",
        aboutEvent: "Unauthorized update"
    ) {
        success
        message
    }
}
```

#### Response:
```json
{
    "data": {
        "updateEventDetail": {
            "success": false,
            "message": "You do not have permission to update this event."
        }
    }
}
```

---

### Description:
- `eventId`: The ID of the event to be updated.
- `phone`: The phone number of the user attempting to update the event.
- Additional fields depend on the user's role:
  - **Owner** can update all fields.
  - **Admin** can update only the allowed fields.

---

## Query: Filtered Events

The `filteredEvents` query allows you to dynamically filter events using the following criteria:
- `city` (required): The city where the events are located.
- `event_category` (optional): The category of the events.
- `neighborhood` (optional): The neighborhood of the events.
- `has_image` (optional): Whether the events have an associated image.

### Request (By City Only):
```graphql
query {
    filteredEvents(city: "Tehran") {
        id
        title
        eventCategory
        subscriberCount
        startDate
        neighborhood
        image
    }
}
```

#### Response:
```json
{
    "data": {
        "filteredEvents": [
            {
                "id": 45,
                "title": "Event 45",
                "eventCategory": "education",
                "subscriberCount": 75,
                "startDate": "2024-13-22T10:00:00+00:00",
                "neighborhood": "نارمک",
                "image": "event_images/event45.jpg"
            },
            {
                "id": 98,
                "title": "Event 98",
                "eventCategory": "education",
                "subscriberCount": 150,
                "startDate": "2025-17-22T10:00:00+00:00",
                "neighborhood": "باغ فیض",
                "image": "event_images/event98.jpg"
            },
            {
                "id": 33,
                "title": "Event 33",
                "eventCategory": "Entertainment",
                "subscriberCount": 20,
                "startDate": "2025-19-22T10:00:00+00:00",
                "neighborhood": "امیریه",
                "image": "event_images/event33.jpg"
            }
        ]
    }
}
```

---

### Request (By City and Category):
```graphql
query {
    filteredEvents(city: "Tehran", eventCategory: "education") {
        title
        eventCategory
        startDate
    }
}
```

#### Response:
```json
{
    "data": {
        "filteredEvents": [
            {
                "id": 45,
                "title": "Event 45",
                "eventCategory": "education",
                "subscriberCount": 75,
                "startDate": "2024-13-22T10:00:00+00:00",
                "neighborhood": "نارمک",
                "image": "event_images/event45.jpg"
            },
            {
                "id": 98,
                "title": "Event 98",
                "eventCategory": "education",
                "subscriberCount": 150,
                "startDate": "2025-17-22T10:00:00+00:00",
                "neighborhood": "باغ فیض",
                "image": "event_images/event98.jpg"
            }
        ]
    }
}
```

---

### Request (By City and Neighborhood):
```graphql
query {
    filteredEvents(city: "Tehran", neighborhood: "باغ فیض") {
        title
        neighborhood
        startDate
    }
}
```

#### Response:
```json
{
    "data": {
        "filteredEvents": [
            {
                "id": 47,
                "title": "Event 47",
                "eventCategory": "education",
                "subscriberCount": 75,
                "startDate": "2025-02-22T10:00:00+00:00",
                "neighborhood": "باغ فیض",
                "image": "event_images/event47.jpg"
            },
            {
                "id": 98,
                "title": "Event 98",
                "eventCategory": "education",
                "subscriberCount": 150,
                "startDate": "2025-17-22T10:00:00+00:00",
                "neighborhood": "باغ فیض",
                "image": "event_images/event98.jpg"
            }
        ]
    }
}
```

---

### Request (By City and Has Image):
```graphql
query {
    filteredEvents(city: "Tehran", hasImage: true) {
        title
        image
        startDate
    }
}
```

#### Response:
```json
{
    "data": {
        "filteredEvents": [
            {
                "title": "Event 3",
                "image": "event3.jpg",
                "startDate": "2024-01-03T10:00:00+00:00"
            },
            {
                "title": "Event 1",
                "image": "event1.jpg",
                "startDate": "2024-01-01T10:00:00+00:00"
            }
        ]
    }
}
```

---

### Request (By All Filters):
```graphql
query {
    filteredEvents(
        city: "Tehran",
        eventCategory: "education",
        neighborhood: "Neighborhood 1",
        hasImage: true
    ) {
        title
        city
        eventCategory
        neighborhood
        image
        startDate
    }
}
```

#### Response:
```json
{
    "data": {
        "filteredEvents": [
            {
                "title": "Event 1",
                "city": "Tehran",
                "eventCategory": "education",
                "neighborhood": "Neighborhood 1",
                "image": "event_images/event1.jpg",
                "startDate": "2024-01-01T10:00:00+00:00"
            }
        ]
    }
}
```

### Description:
- `city`: The city where the events are located (required).
- `eventCategory`: The category of the events (optional).
- `neighborhood`: The neighborhood of the events (optional).
- `hasImage`: Whether the events have an associated image (optional).


## Mutation: Request Join Event

The `requestJoinEvent` mutation allows a user to request to join an event.

### Request:
```graphql
mutation {
    requestJoinEvent(eventId: "1", phone: "09123456789") {
        success
        message
    }
}
```

### Response:
#### Successful Request:
```json
{
    "data": {
        "requestJoinEvent": {
            "success": true,
            "message": "Request to join the event has been sent successfully."
        }
    }
}
```

#### Duplicate Request:
If the user has already requested to join the event:
```json
{
    "data": {
        "requestJoinEvent": {
            "success": false,
            "message": "You have already requested to join this event."
        }
    }
}
```

---

## Mutation: Review Join Request

The `reviewJoinRequest` mutation allows the owner of an event to approve or reject a user's join request and optionally assign a role.

### Request:
#### Approve Request:
```graphql
mutation {
    reviewJoinRequest(
        eventId: "1",
        userId: "2",
        action: "approve",
        role: "admin",
        ownerPhone: "09123456788"
    ) {
        success
        message
    }
}
```

#### Reject Request:
```graphql
mutation {
    reviewJoinRequest(
        eventId: "1",
        userId: "2",
        action: "reject",
        ownerPhone: "09123456788"
    ) {
        success
        message
    }
}
```

### Responses:
#### Approve Request:
```json
{
    "data": {
        "reviewJoinRequest": {
            "success": true,
            "message": "User request approved successfully with role 'admin'."
        }
    }
}
```

#### Reject Request:
```json
{
    "data": {
        "reviewJoinRequest": {
            "success": true,
            "message": "User request rejected successfully."
        }
    }
}
```

#### Invalid Action:
If an invalid action is provided:
```json
{
    "data": {
        "reviewJoinRequest": {
            "success": false,
            "message": "Invalid action provided."
        }
    }
}
```

---

### Description:
#### Request Join Event:
- `eventId`: The ID of the event the user wants to join.
- `phone`: The phone number of the user.
- **Behavior:**
  - Creates a join request with `is_approved=None` (pending status).
  - Returns a message indicating success or failure (e.g., duplicate request).

#### Review Join Request:
- `eventId`: The ID of the event the request is related to.
- `userId`: The ID of the user whose request is being reviewed.
- `action`: The action to take on the request (`approve` or `reject`).
- `role` (optional): The role to assign to the user if the request is approved (`regular` or `admin`).
- `ownerPhone`: The phone number of the event owner.
- **Behavior:**
  - Allows the owner to approve or reject requests.
  - Sets the `role` if the request is approved.

---


## Query: Check Join Request Status

The `checkJoinRequestStatus` query allows you to check the status of a user's join request for a specific event.

### Request:
```graphql
query {
    checkJoinRequestStatus(phone: "09123456789", eventId: "1") {
        message
    }
}
```

### Responses:

#### Pending Request:
If the request is still pending review:
```json
{
    "data": {
        "checkJoinRequestStatus": {
            "message": "Your request is pending review."
        }
    }
}
```

#### Rejected Request:
If the request has been rejected:
```json
{
    "data": {
        "checkJoinRequestStatus": {
            "message": "Your request has been rejected."
        }
    }
}
```

#### Approved Request as Regular User:
If the request has been approved and the user is assigned the `regular` role:
```json
{
    "data": {
        "checkJoinRequestStatus": {
            "message": "Your request has been approved as a regular user."
        }
    }
}
```

#### Approved Request as Admin:
If the request has been approved and the user is assigned the `admin` role:
```json
{
    "data": {
        "checkJoinRequestStatus": {
            "message": "Your request has been approved as an admin user."
        }
    }
}
```

#### No Request Found:
If no join request exists for the user and event:
```json
{
    "data": {
        "checkJoinRequestStatus": {
            "message": "No join request found for this event."
        }
    }
}
```

---

### Description:
- `phone`: The phone number of the user whose join request status you want to check.
- `eventId`: The ID of the event for which the join request status is being checked.

### Behavior:
- Returns a message indicating the current status of the join request:
  - Pending (`is_approved=None`): "Your request is pending review."
  - Rejected (`is_approved=False`): "Your request has been rejected."
  - Approved as Regular User (`is_approved=True` and `role=regular`): "Your request has been approved as a regular user."
  - Approved as Admin (`is_approved=True` and `role=admin`): "Your request has been approved as an admin user."
  - No Request Found: "No join request found for this event."


## Mutation: Delete Event

The `deleteEvent` mutation allows the owner of an event to delete it based on its ID.

### Request:
```graphql
mutation {
    deleteEvent(eventId: "1", ownerPhone: "09123456789") {
        success
        message
    }
}
```

### Responses:

#### Successful Deletion:
If the owner successfully deletes the event:
```json
{
    "data": {
        "deleteEvent": {
            "success": true,
            "message": "Event deleted successfully."
        }
    }
}
```

#### Unauthorized User:
If a user other than the owner attempts to delete the event:
```json
{
    "data": {
        "deleteEvent": {
            "success": false,
            "message": "You are not authorized to delete this event."
        }
    }
}
```

#### Non-Existent Event:
If the event does not exist:
```json
{
    "data": {
        "deleteEvent": {
            "success": false,
            "message": "Event not found."
        }
    }
}
```

---

### Description:
- `eventId`: The ID of the event to be deleted.
- `ownerPhone`: The phone number of the user attempting to delete the event.

### Behavior:
- **Successful Deletion:** If the user is the owner of the event, the event is deleted, and a success message is returned.
- **Unauthorized User:** If the user is not the owner, the deletion is blocked, and an error message is returned.
- **Non-Existent Event:** If the event ID does not match any existing event, an error message is returned.


## Query: Events by Owner

The `eventsByOwner` query allows you to retrieve all events created by a specific owner using their phone number.

### Request:
```graphql
query {
    eventsByOwner(phone: "09123456789") {
        id
        title
        eventCategory
        startDate
        endDate
        city
        maxSubscribers
    }
}
```

### Responses:

#### Successful Request:
If events exist for the owner:
```json
{
    "data": {
        "eventsByOwner": [
            {
                "id": "1",
                "title": "Event 2",
                "eventCategory": "sport",
                "startDate": "2024-12-23T15:00:00+00:00",
                "endDate": "2024-12-23T20:00:00+00:00",
                "city": "کرج",
                "maxSubscribers": 50
            },
            {
                "id": "2",
                "title": "Event 1",
                "eventCategory": "education",
                "startDate": "2024-12-22T10:00:00+00:00",
                "endDate": "2024-12-22T18:00:00+00:00",
                "city": "تهران",
                "maxSubscribers": 100
            }
        ]
    }
}
```

#### No Events Found:
If the owner has not created any events or the phone number does not exist:
```json
{
    "data": {
        "eventsByOwner": []
    }
}
```

---

### Description:
- **`phone`**: The phone number of the user whose events are being fetched.

### Behavior:
- Returns all events created by the specified owner.
- Each event includes the following fields:
  - `id`: The unique identifier of the event.
  - `title`: The title of the event.
  - `eventCategory`: The category of the event (e.g., education, sport).
  - `startDate` and `endDate`: The start and end dates/times of the event.
  - `city`: The city where the event takes place.
  - `maxSubscribers`: The maximum number of participants allowed for the event.


## Query: User's Approved Events

The `userEvents` query allows you to retrieve all events where the user is approved (`is_approved=True`) and has the role of `regular`.

### Request:
```graphql
query {
    userEvents(phone: "09123456789") {
        id
        title
        eventCategory
        startDate
        endDate
        city
        maxSubscribers
    }
}
```

### Responses:

#### Successful Request:
If events exist for the user:
```json
{
    "data": {
        "userEvents": [
            {
                "id": "1",
                "title": "Event 2",
                "eventCategory": "sport",
                "startDate": "2024-12-23T15:00:00+00:00",
                "endDate": "2024-12-23T20:00:00+00:00",
                "city": "کرج",
                "maxSubscribers": 50
            },
            {
                "id": "2",
                "title": "Event 1",
                "eventCategory": "education",
                "startDate": "2024-12-22T10:00:00+00:00",
                "endDate": "2024-12-22T18:00:00+00:00",
                "city": "تهران",
                "maxSubscribers": 100
            }
        ]
    }
}
```

#### No Events Found:
If the user has no approved events or the phone number does not exist:
```json
{
    "data": {
        "userEvents": []
    }
}
```

---

### Description:
- **`phone`**: The phone number of the user whose approved events are being fetched.

### Behavior:
- Returns all events where:
  - The user is approved (`is_approved=True`).
  - The user has the role `regular`.
- Each event includes the following fields:
  - `id`: The unique identifier of the event.
  - `title`: The title of the event.
  - `eventCategory`: The category of the event (e.g., education, sport).
  - `startDate` and `endDate`: The start and end dates/times of the event.
  - `city`: The city where the event takes place.
  - `maxSubscribers`: The maximum number of participants allowed for the event.


## Query: User's Admin Events

The `adminEvents` query allows you to retrieve all events where the user is approved (`is_approved=True`) and has the role of `admin`.

### Request:
```graphql
query {
    adminEvents(phone: "09123456789") {
        id
        title
        eventCategory
        startDate
        endDate
        city
        maxSubscribers
    }
}
```

### Responses:

#### Successful Request:
If events exist for the user as an admin:
```json
{
    "data": {
        "adminEvents": [
            {
                "id": "1",
                "title": "Admin Event 2",
                "eventCategory": "technology",
                "startDate": "2024-12-23T15:00:00+00:00",
                "endDate": "2024-12-23T20:00:00+00:00",
                "city": "کرج",
                "maxSubscribers": 50
            },
            {
                "id": "2",
                "title": "Admin Event 1",
                "eventCategory": "management",
                "startDate": "2024-12-22T10:00:00+00:00",
                "endDate": "2024-12-22T18:00:00+00:00",
                "city": "تهران",
                "maxSubscribers": 100
            }
        ]
    }
}
```

#### No Events Found:
If the user has no admin events or the phone number does not exist:
```json
{
    "data": {
        "adminEvents": []
    }
}
```

---

### Description:
- **`phone`**: The phone number of the user whose admin events are being fetched.

### Behavior:
- Returns all events where:
  - The user is approved (`is_approved=True`).
  - The user has the role `admin`.
- Each event includes the following fields:
  - `id`: The unique identifier of the event.
  - `title`: The title of the event.
  - `eventCategory`: The category of the event (e.g., technology, management).
  - `startDate` and `endDate`: The start and end dates/times of the event.
  - `city`: The city where the event takes place.
  - `maxSubscribers`: The maximum number of participants allowed for the event.


---

This document provides the necessary information to test and implement the GraphQL API interactions for event management in your project.
