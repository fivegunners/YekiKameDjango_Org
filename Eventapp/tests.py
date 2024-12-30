import graphene
from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import Event, Review, Comment, UserEventRole, EventFeature
from datetime import datetime, timedelta
from userapp.models import User  # اضافه کردن مدل User
from django.utils.timezone import make_aware


class EventSchemaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت یک کاربر تستی با استفاده از متد create_user
        cls.user = User.objects.create_user(phone="09123456789", password="password123")

        # ساخت رویدادهای تست برای استفاده در کوئری‌ها با مقادیر start_date و end_date
        Event.objects.create(
            title="Event in Tehran",
            event_category="education",
            city="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date=datetime.now(),
            registration_end_date=datetime.now() + timedelta(days=1),
            max_subscribers=100,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            neighborhood="تهرانپارس",
            event_owner=cls.user
        )
        Event.objects.create(
            title="Event in Mashhad",
            event_category="sport",
            city="مشهد",
            postal_address="مشهد، خیابان امام رضا (ع)",
            postal_code="4871592630",
            registration_start_date=datetime.now(),
            registration_end_date=datetime.now() + timedelta(days=1),
            max_subscribers=50,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            event_owner=cls.user
        )
        Event.objects.create(
            title="Event in Shiraz",
            event_category="game",
            city="شیراز",
            postal_address="شیراز، بلوار حافظ",
            postal_code="2631598470",
            registration_start_date=datetime.now(),
            registration_end_date=datetime.now() + timedelta(days=1),
            max_subscribers=80,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_search_events_by_city(self):
        # تست کوئری برای جستجو بر اساس شهر
        query = '''
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
        '''
        response = self.client.execute(query)
        data = response.get("data").get("searchEventsByCity")

        self.assertIsNotNone(data[0]["id"], "ID should not be None")
        self.assertNotEqual(data[0]["id"], "", "ID should not be empty")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Event in Tehran")
        self.assertEqual(data[0]["eventCategory"], "EDUCATION")
        self.assertEqual(data[0]["neighborhood"], "تهرانپارس")
        self.assertIn("subscriberCount", data[0])
        self.assertIn("startDate", data[0])

    def test_recent_events(self):
        # تست کوئری برای دریافت رویدادهای اخیر
        query = '''
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
        '''
        response = self.client.execute(query)
        #print(response)
        data = response.get("data", {}).get("recentEvents", {})
        #print(data)

        # بررسی اینکه recentEvents داده‌ای دارد
        self.assertIsNotNone(data, "The recentEvents query returned None")

        # بررسی تعداد رویدادهای برگردانده شده
        self.assertGreaterEqual(len(data), 3)
        self.assertIsNotNone(data[0]["id"], "ID should not be None")
        self.assertNotEqual(data[0]["id"], "", "ID should not be empty")
        self.assertEqual(data[0]["title"], "Event in Shiraz")
        self.assertIn("subscriberCount", data[0])
        self.assertIn("startDate", data[0])
        self.assertIn("neighborhood", data[0])
        self.assertIn("eventCategory", data[0])

    def test_create_event_mutation(self):
        # تست Mutation برای ایجاد رویداد جدید
        mutation = '''
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
                    id
                    title
                    eventCategory
                    maxSubscribers
                    startDate
                    neighborhood
                }
            }
        }
        '''
        response = self.client.execute(mutation)
        event_data = response.get("data", {}).get("createEvent", {}).get("event")

        # بررسی اینکه event_data خالی نیست
        self.assertIsNotNone(event_data, "The createEvent mutation returned None")

        # بررسی محتوای رویداد ایجاد شده
        self.assertEqual(event_data["title"], "New Event")
        self.assertEqual(event_data["eventCategory"], "ENTERTAINMENT")
        self.assertEqual(event_data["neighborhood"], "District 1")
        self.assertEqual(event_data["startDate"], "2024-12-01T09:00:00+00:00")
        self.assertEqual(event_data["maxSubscribers"], 150)


class TestReviewAndCommentMutations(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تست
        cls.user = User.objects.create_user(phone="09123456789", password="password123")

        # ساخت رویداد تست
        cls.event = Event.objects.create(
            title="Event in Tehran",
            event_category="education",
            city="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date=datetime.now(),
            registration_end_date=datetime.now() + timedelta(days=1),
            max_subscribers=100,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            neighborhood="تهرانپارس",
            event_owner=cls.user
        )
        # ساخت چندین Review برای رویداد
        review1 = Review.objects.create(event=cls.event, user=cls.user, rating=4.3, comment_text="Great event!")
        review2 = Review.objects.create(event=cls.event, user=cls.user, rating=3.2, comment_text="It was okay.")
        review3 = Review.objects.create(event=cls.event, user=cls.user, rating=1.0, comment_text="Absolutely Bad!")

        # تنظیم مقادیر created_at به صورت دستی
        review1.created_at = datetime.now() - timedelta(days=4)
        review2.created_at = datetime.now() - timedelta(days=2)
        review3.created_at = datetime.now()

        review1.save()
        review2.save()
        review3.save()

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_create_review_mutation(self):
        # تعریف Mutation برای ایجاد Review
        mutation = """
            mutation {
                createReview(eventId: "%s", userId: "%s", rating: 4.5, commentText: "This is a great event!") {
                    review {
                        id
                        rating
                        commentText
                    }
                }
            }
        """ % (self.event.id, self.user.id)

        # ارسال درخواست به GraphQL
        response = self.client.execute(mutation)
        #print(response)
        # استخراج داده‌های پاسخ
        response_data = response.get("data", {}).get("createReview", {}).get("review")
        #print(response_data)
        # بررسی پاسخ
        self.assertIsNotNone(response_data)  # بررسی که داده‌ها برگشت داده شده‌اند
        self.assertEqual(response_data["rating"], 4.5)
        self.assertEqual(response_data["commentText"], "This is a great event!")  # بررسی که متن نظر درست است

    def test_create_comment_mutation(self):
        # ابتدا یک Review برای تست کامنت ایجاد می‌کنیم
        review = Review.objects.create(
            event=self.event,
            user=self.user,
            rating=5,
            comment_text="This is a great event!"
        )

        # تعریف Mutation برای ایجاد Comment
        mutation = """
            mutation {
                createComment(reviewId: "%s", userId: "%s", commentText: "I agree with this review!", isActive: true) {
                    comment {
                        id
                        commentText
                        isActive
                        level
                    }
                }
            }
        """ % (review.id, self.user.id)

        # ارسال درخواست به GraphQL
        response = self.client.execute(mutation)

        # استخراج داده‌های پاسخ
        response_data = response.get("data", {}).get("createComment", {}).get("comment")

        # بررسی پاسخ
        self.assertIsNotNone(response_data)  # بررسی که داده‌ها برگشت داده شده‌اند
        self.assertEqual(response_data["commentText"], "I agree with this review!")  # بررسی که متن کامنت درست است
        self.assertTrue(response_data["isActive"])  # بررسی که فیلد isActive درست است
        self.assertEqual(response_data["level"], 1)  # بررسی که سطح کامنت 1 است (نظر اصلی)

    def test_create_reply_to_comment(self):
        # ابتدا یک Review برای تست کامنت ایجاد می‌کنیم
        review = Review.objects.create(
            event=self.event,
            user=self.user,
            rating=5,
            comment_text="This is a great event!"
        )

        # ایجاد اولین کامنت
        comment = Comment.objects.create(
            review=review,
            user=self.user,
            comment_text="First comment",
            level=1
        )

        # تعریف Mutation برای ایجاد کامنت به عنوان پاسخ (ریپلای)
        mutation = """
            mutation {
                createComment(reviewId: "%s", userId: "%s", commentText: "This is a reply!", parentCommentId: "%s", isActive: true) {
                    comment {
                        id
                        commentText
                        isActive
                        level
                    }
                }
            }
        """ % (review.id, self.user.id, comment.id)

        # ارسال درخواست به GraphQL
        response = self.client.execute(mutation)

        # استخراج داده‌های پاسخ
        response_data = response.get("data", {}).get("createComment", {}).get("comment")

        # بررسی پاسخ
        self.assertIsNotNone(response_data)  # بررسی که داده‌ها برگشت داده شده‌اند
        self.assertEqual(response_data["commentText"], "This is a reply!")  # بررسی که متن ریپلای درست است
        self.assertTrue(response_data["isActive"])  # بررسی که فیلد isActive درست است
        self.assertEqual(response_data["level"], 2)  # بررسی که سطح ریپلای برابر با ۲ است (پاسخ به نظر اصلی)

    def test_reviews_by_event_query(self):
        # تست کوئری برای دریافت تمام Reviews مربوط به یک Event
        query = '''
        query {
            reviewsByEvent(eventId: "%s") {
                id
                rating
                commentText
                createdAt
            }
        }
        ''' % self.event.id

        response = self.client.execute(query)
        data = response.get("data", {}).get("reviewsByEvent", [])

        # بررسی پاسخ
        self.assertEqual(len(data), 3, "There should be 3 reviews for the event.")
        self.assertEqual(data[0]["rating"], 1.0, "The first review should have the most recent created_at.")
        self.assertEqual(data[1]["rating"], 3.2, "The second review should have the middle created_at.")
        self.assertEqual(data[2]["rating"], 4.3, "The third review should have the oldest created_at.")
        self.assertIsNotNone(data[0]["createdAt"], "The createdAt field should not be None.")


class CommentSchemaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت یک کاربر تستی با استفاده از متد create_user
        cls.user = User.objects.create_user(phone="09123456789", password="password123")

        # ساخت رویداد تستی
        cls.event = Event.objects.create(
            title="Event in Tehran",
            event_category="education",
            city="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date=datetime.now(),
            registration_end_date=datetime.now() + timedelta(days=1),
            max_subscribers=100,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            neighborhood="تهرانپارس",
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_comments_by_review_query(self):
        # ساخت یک Review تستی
        review = Review.objects.create(
            event=self.event,
            user=self.user,
            rating=4.5,
            comment_text="Great event!",
            created_at=datetime.now() - timedelta(days=10)
        )

        # ساخت چندین Comment تستی
        comment1 = Comment.objects.create(
            review=review,
            user=self.user,
            comment_text="Loved it!",
            level=1,
            is_active=True
        )
        comment2 = Comment.objects.create(
            review=review,
            user=self.user,
            comment_text="It was okay.",
            level=1,
            is_active=True
        )
        comment3 = Comment.objects.create(
            review=review,
            user=self.user,
            comment_text="Not great.",
            level=1,
            is_active=True
        )

        # تنظیم مقادیر created_at به صورت دستی
        comment1.created_at = datetime.now() - timedelta(days=4)
        comment2.created_at = datetime.now() - timedelta(days=2)
        comment3.created_at = datetime.now()

        comment1.save()
        comment2.save()
        comment3.save()

        # تست کوئری برای دریافت تمام Comments مربوط به یک Review
        query = '''
        query {
            commentsByReview(reviewId: "%s") {
                id
                commentText
                createdAt
                level
                isActive
            }
        }
        ''' % review.id

        response = self.client.execute(query)
        data = response.get("data", {}).get("commentsByReview", [])
        #print(data)

        # بررسی پاسخ
        self.assertEqual(len(data), 3, "There should be 3 comments for the review.")
        self.assertEqual(data[0]["commentText"], "Not great.",
                         "The first comment should have the most recent created_at.")
        self.assertEqual(data[1]["commentText"], "It was okay.",
                         "The second comment should have the middle created_at.")
        self.assertEqual(data[2]["commentText"], "Loved it!", "The third comment should have the oldest created_at.")
        self.assertTrue(data[0]["isActive"], "The isActive field should be True.")
        self.assertEqual(data[0]["level"], 1, "The level field should be 1.")


class EventDetailPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت یک کاربر تستی با استفاده از متد create_user
        cls.user = User.objects.create_user(phone="09123456789", password="password123")

        # تاریخ‌های تستی به صورت دستی
        cls.start_date = datetime(2024, 12, 22, 10, 0, 0)
        cls.end_date = datetime(2024, 12, 22, 18, 0, 0)
        cls.registration_start_date = datetime(2024, 12, 20, 10, 0, 0)
        cls.registration_end_date = datetime(2024, 12, 21, 18, 0, 0)

        # ساخت رویداد تستی با تمام فیلدها
        cls.event = Event.objects.create(
            title="Event in Tehran",
            event_category="education",
            about_event="This is a detailed description of the event.",
            image=None,  # بدون تصویر
            start_date=cls.start_date,
            end_date=cls.end_date,
            province="تهران",
            city="تهران",
            neighborhood="تهرانپارس",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date=cls.registration_start_date,
            registration_end_date=cls.registration_end_date,
            full_description="This is the full description of the event.",
            max_subscribers=100,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_event_details_query(self):
        # تست کوئری برای دریافت اطلاعات کامل یک Event
        query = '''
        query {
            eventDetails(eventId: "%s") {
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
        ''' % self.event.id

        response = self.client.execute(query)
        data = response.get("data", {}).get("eventDetails", {})

        # بررسی اینکه خطایی وجود ندارد
        self.assertIsNone(data["error"], "Error field should be None.")

        # بررسی فیلدهای رویداد
        event_data = data.get("event", {})
        self.assertEqual(event_data["id"], str(self.event.id), "Event ID should match.")
        self.assertEqual(event_data["title"], self.event.title, "Event title should match.")
        self.assertEqual(event_data["eventCategory"], self.event.event_category, "Event category should match.")
        self.assertEqual(event_data["aboutEvent"], self.event.about_event, "Event about field should match.")
        self.assertEqual(event_data["startDate"], "2024-12-22T10:00:00+00:00", "Event start date should match.")
        self.assertEqual(event_data["endDate"], "2024-12-22T18:00:00+00:00", "Event end date should match.")
        self.assertEqual(event_data["province"], self.event.province, "Event province should match.")
        self.assertEqual(event_data["city"], self.event.city, "Event city should match.")
        self.assertEqual(event_data["neighborhood"], self.event.neighborhood, "Event neighborhood should match.")
        self.assertEqual(event_data["postalAddress"], self.event.postal_address, "Event postal address should match.")
        self.assertEqual(event_data["postalCode"], self.event.postal_code, "Event postal code should match.")
        self.assertEqual(event_data["registrationStartDate"], "2024-12-20T10:00:00+00:00", "Event registration start date should match.")
        self.assertEqual(event_data["registrationEndDate"], "2024-12-21T18:00:00+00:00", "Event registration end date should match.")
        self.assertEqual(event_data["fullDescription"], self.event.full_description, "Event full description should match.")
        self.assertEqual(event_data["maxSubscribers"], self.event.max_subscribers, "Event max subscribers should match.")
        self.assertEqual(event_data["eventOwner"]["phone"], self.event.event_owner.phone, "Event owner phone should match.")


class RelatedEventsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت ایونت اصلی
        cls.main_event = Event.objects.create(
            title="Main Event",
            event_category="education",
            about_event="This is the main event.",
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            province="تهران",
            city="تهران",
            neighborhood="تهرانپارس",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date=datetime.now() - timedelta(days=1),
            registration_end_date=datetime.now(),
            full_description="This is the full description of the main event.",
            max_subscribers=100,
            event_owner=cls.user
        )

        # ساخت ایونت‌های مرتبط با همان دسته‌بندی
        for i in range(7):
            Event.objects.create(
                title=f"Related Event {i+1}",
                event_category="education",
                about_event=f"This is related event {i+1}.",
                start_date=datetime.now() + timedelta(days=1),
                end_date=datetime.now() + timedelta(days=2),
                province="تهران",
                city="تهران",
                neighborhood=f"Neighborhood {i+1}",
                postal_address=f"Address {i+1}",
                postal_code=f"159263478{i}",
                registration_start_date=datetime.now() - timedelta(days=1),
                registration_end_date=datetime.now(),
                full_description=f"Full description for related event {i+1}.",
                max_subscribers=50,
                event_owner=cls.user
            )

        # ساخت یک ایونت غیرمرتبط
        Event.objects.create(
            title="Unrelated Event",
            event_category="sport",
            about_event="This is an unrelated event.",
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            province="تهران",
            city="تهران",
            neighborhood="Different Neighborhood",
            postal_address="Different Address",
            postal_code="1234567890",
            registration_start_date=datetime.now() - timedelta(days=1),
            registration_end_date=datetime.now(),
            full_description="This is the full description of the unrelated event.",
            max_subscribers=50,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_related_events_query(self):
        # کوئری برای دریافت ایونت‌های مرتبط
        query = '''
        query {
            relatedEvents(eventId: "%s") {
                title
                eventCategory
            }
        }
        ''' % self.main_event.id

        response = self.client.execute(query)
        related_events = response.get("data", {}).get("relatedEvents", [])

        # بررسی تعداد ایونت‌های بازگشتی
        self.assertLessEqual(len(related_events), 5, "There should be at most 5 related events.")

        # بررسی اینکه همه ایونت‌های بازگشتی از یک دسته‌بندی هستند
        for event in related_events:
            self.assertEqual(event["eventCategory"], "EDUCATION", "All related events should have the same category.")


class TestSearchEventsbyCityandCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت ایونت‌ها
        event1 = Event.objects.create(
            title="Event 1",
            event_category="education",
            city="Tehran",
            about_event="This is Event 1.",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            province="تهران",
            neighborhood="تهرانپارس",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date="2024-01-01 10:00:00",
            registration_end_date="2024-01-04 18:00:00",
            full_description="This is the full description of Event 1.",
            max_subscribers=100,
            event_owner=cls.user
        )
        event1.start_date = "2024-01-01 10:00:00"
        event1.save()

        event2 = Event.objects.create(
            title="Event 2",
            event_category="education",
            city="Tehran",
            about_event="This is Event 2.",
            start_date="2024-01-02 10:00:00",
            end_date="2024-01-06 18:00:00",
            province="تهران",
            neighborhood="تهرانپارس",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634781",
            registration_start_date="2024-01-02 10:00:00",
            registration_end_date="2024-01-05 18:00:00",
            full_description="This is the full description of Event 2.",
            max_subscribers=50,
            event_owner=cls.user
        )
        event2.start_date = "2024-01-02 10:00:00"
        event2.save()

        event3 = Event.objects.create(
            title="Event 3",
            event_category="sport",
            city="Tehran",
            about_event="This is Event 3.",
            start_date="2024-01-03 10:00:00",
            end_date="2024-01-07 18:00:00",
            province="تهران",
            neighborhood="تهرانپارس",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634782",
            registration_start_date="2024-01-03 10:00:00",
            registration_end_date="2024-01-06 18:00:00",
            full_description="This is the full description of Event 3.",
            max_subscribers=30,
            event_owner=cls.user
        )
        event3.start_date = "2024-01-03 10:00:00"
        event3.save()

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_events_by_city_and_category(self):
        # کوئری برای دریافت ایونت‌ها
        query = '''
        query {
            eventsByCityAndCategory(city: "Tehran", category: "education") {
                title
                eventCategory
                startDate
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("eventsByCityAndCategory", [])

        # بررسی تعداد ایونت‌های بازگشتی
        self.assertEqual(len(events), 2, "There should be 2 events matching the city and category.")

        # بررسی ترتیب ایونت‌ها بر اساس start_date
        self.assertEqual(events[0]["title"], "Event 2", "The most recently started event should come first.")
        self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

        # بررسی دسته‌بندی و شهر ایونت‌ها
        for event in events:
            self.assertEqual(event["eventCategory"], "EDUCATION", "All events should have the category 'education'.")


class TestSearchEventsbyCityandNeighborhood(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت ایونت‌ها
        Event.objects.create(
            title="Event 1",
            event_category="education",
            city="Tehran",
            neighborhood="Neighborhood 1",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            about_event="This is Event 1.",
            province="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date="2024-01-01 10:00:00",
            registration_end_date="2024-01-04 18:00:00",
            full_description="This is the full description of Event 1.",
            max_subscribers=100,
            event_owner=cls.user
        )

        Event.objects.create(
            title="Event 2",
            event_category="education",
            city="Tehran",
            neighborhood="Neighborhood 1",
            start_date="2024-01-02 10:00:00",
            end_date="2024-01-06 18:00:00",
            about_event="This is Event 2.",
            province="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634781",
            registration_start_date="2024-01-02 10:00:00",
            registration_end_date="2024-01-05 18:00:00",
            full_description="This is the full description of Event 2.",
            max_subscribers=50,
            event_owner=cls.user
        )

        Event.objects.create(
            title="Event 3",
            event_category="sport",
            city="Tehran",
            neighborhood="Neighborhood 2",
            start_date="2024-01-03 10:00:00",
            end_date="2024-01-07 18:00:00",
            about_event="This is Event 3.",
            province="تهران",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634782",
            registration_start_date="2024-01-03 10:00:00",
            registration_end_date="2024-01-06 18:00:00",
            full_description="This is the full description of Event 3.",
            max_subscribers=30,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_events_by_city_and_neighborhood(self):
        # کوئری برای دریافت ایونت‌ها
        query = '''
        query {
            eventsByCityAndNeighborhood(city: "Tehran", neighborhood: "Neighborhood 1") {
                title
                city
                neighborhood
                startDate
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("eventsByCityAndNeighborhood", [])

        # بررسی تعداد ایونت‌های بازگشتی
        self.assertEqual(len(events), 2, "There should be 2 events matching the city and neighborhood.")

        # بررسی ترتیب ایونت‌ها بر اساس start_date
        self.assertEqual(events[0]["title"], "Event 2", "The most recently started event should come first.")
        self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

        # بررسی شهر و محله ایونت‌ها
        for event in events:
            self.assertEqual(event["city"], "Tehran", "All events should be in the city 'Tehran'.")
            self.assertEqual(event["neighborhood"], "Neighborhood 1", "All events should be in the neighborhood 'Neighborhood 1'.")


class TestEventsWithImagesByCity(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت ایونت‌ها
        Event.objects.create(
            title="Event 1",
            event_category="education",
            city="Tehran",
            image="event1.jpg",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            about_event="This is Event 1.",
            province="تهران",
            neighborhood="Neighborhood 1",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634780",
            registration_start_date="2024-01-01 10:00:00",
            registration_end_date="2024-01-04 18:00:00",
            full_description="This is the full description of Event 1.",
            max_subscribers=100,
            event_owner=cls.user
        )

        Event.objects.create(
            title="Event 2",
            event_category="education",
            city="Tehran",
            image="",
            start_date="2024-01-02 10:00:00",
            end_date="2024-01-06 18:00:00",
            about_event="This is Event 2.",
            province="تهران",
            neighborhood="Neighborhood 2",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634781",
            registration_start_date="2024-01-02 10:00:00",
            registration_end_date="2024-01-05 18:00:00",
            full_description="This is the full description of Event 2.",
            max_subscribers=50,
            event_owner=cls.user
        )

        Event.objects.create(
            title="Event 3",
            event_category="sport",
            city="Tehran",
            image="event3.jpg",
            start_date="2024-01-03 10:00:00",
            end_date="2024-01-07 18:00:00",
            about_event="This is Event 3.",
            province="تهران",
            neighborhood="Neighborhood 3",
            postal_address="تهرانپارس، خیابان ۱۷۴ غربی",
            postal_code="1592634782",
            registration_start_date="2024-01-03 10:00:00",
            registration_end_date="2024-01-06 18:00:00",
            full_description="This is the full description of Event 3.",
            max_subscribers=30,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_events_with_images_by_city(self):
        # کوئری برای دریافت ایونت‌ها
        query = '''
        query {
            eventsWithImagesByCity(city: "Tehran") {
                title
                city
                image
                startDate
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("eventsWithImagesByCity", [])
        print(events)

        # بررسی تعداد ایونت‌های بازگشتی
        self.assertEqual(len(events), 2, "There should be 2 events with images in the city.")

        # بررسی ترتیب ایونت‌ها بر اساس start_date
        self.assertEqual(events[0]["title"], "Event 3", "The most recently started event should come first.")
        self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

        # بررسی شهر و داشتن تصویر
        for event in events:
            self.assertEqual(event["city"], "Tehran", "All events should be in the city 'Tehran'.")
            self.assertIsNotNone(event["image"], "All events should have an image.")
