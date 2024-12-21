import graphene
from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import Event, Review, Comment, UserEventRole, EventFeature
from datetime import datetime, timedelta
from userapp.models import User  # اضافه کردن مدل User


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
        print(data)

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
        print(response)
        # استخراج داده‌های پاسخ
        response_data = response.get("data", {}).get("createReview", {}).get("review")
        print(response_data)
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