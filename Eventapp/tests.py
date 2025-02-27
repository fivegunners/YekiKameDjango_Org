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
                image: null,
                startDate: "2024-12-01T09:00:00Z",
                endDate: "2024-12-01T17:00:00Z",
                registrationStartDate: "2024-11-01T09:00:00Z",
                registrationEndDate: "2024-11-25T17:00:00Z",
                province: "تهران",
                city: "تهران",
                neighborhood: "District 1",
                postalAddress: "Some Street, Tehran",
                postalCode: "1234567890",
                fullDescription: "This is the full description of the event.",
                maxSubscribers: 150,
                eventOwnerPhone: "09123456789"
            ) {
                event {
                    id
                    title
                    eventCategory
                    aboutEvent
                    image
                    startDate
                    endDate
                    registrationStartDate
                    registrationEndDate
                    province
                    city
                    neighborhood
                    postalAddress
                    postalCode
                    fullDescription
                    maxSubscribers
                    eventOwner {
                        phone
                    }
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
        self.assertEqual(event_data["aboutEvent"], "A new entertainment event.")
        self.assertIn(event_data["image"], [None, ""], "Image should be None or an empty string")
        self.assertEqual(event_data["startDate"], "2024-12-01T09:00:00+00:00")
        self.assertEqual(event_data["endDate"], "2024-12-01T17:00:00+00:00")
        self.assertEqual(event_data["registrationStartDate"], "2024-11-01T09:00:00+00:00")
        self.assertEqual(event_data["registrationEndDate"], "2024-11-25T17:00:00+00:00")
        self.assertEqual(event_data["province"], "تهران")
        self.assertEqual(event_data["city"], "تهران")
        self.assertEqual(event_data["neighborhood"], "District 1")
        self.assertEqual(event_data["postalAddress"], "Some Street, Tehran")
        self.assertEqual(event_data["postalCode"], "1234567890")
        self.assertEqual(event_data["fullDescription"], "This is the full description of the event.")
        self.assertEqual(event_data["maxSubscribers"], 150)
        self.assertEqual(event_data["eventOwner"]["phone"], "09123456789")


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


class TestUpdateEventDetail(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربران تستی
        cls.owner = User.objects.create_user(
            phone="09123456789",
            password="ownerpassword"
        )

        cls.admin = User.objects.create_user(
            phone="09123456788",
            password="adminpassword"
        )

        cls.other_user = User.objects.create_user(
            phone="09123456787",
            password="otherpassword"
        )

        # ساخت ایونت تستی
        cls.event = Event.objects.create(
            title="Test Event",
            event_category="education",
            about_event="Original description",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            registration_start_date="2023-12-20 10:00:00",
            registration_end_date="2023-12-30 18:00:00",
            full_description="Original full description",
            max_subscribers=100,
            event_owner=cls.owner
        )

        # اختصاص نقش ادمین به کاربر
        UserEventRole.objects.create(user=cls.admin, event=cls.event, role="admin")

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_update_event_by_owner(self):
        # کوئری برای به‌روزرسانی ایونت توسط Owner
        query = '''
        mutation {
            updateEventDetail(
                eventId: "%s",
                phone: "%s",
                title: "Updated Event Title",
                aboutEvent: "Updated description",
                startDate: "2024-01-02 10:00:00"
            ) {
                success
                message
            }
        }
        ''' % (self.event.id, self.owner.phone)

        response = self.client.execute(query)
        data = response.get("data", {}).get("updateEventDetail", {})

        # بررسی موفقیت‌آمیز بودن عملیات
        self.assertTrue(data["success"], "Owner should be able to update all fields.")
        self.assertEqual(data["message"], "Event updated successfully by the owner.")

        # بررسی تغییرات ایونت
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Event Title", "Title should be updated.")
        self.assertEqual(self.event.about_event, "Updated description", "About event should be updated.")
        self.assertEqual(str(self.event.start_date), "2024-01-02 10:00:00+00:00", "Start date should be updated.")

    def test_update_event_by_admin(self):
        # کوئری برای به‌روزرسانی ایونت توسط Admin
        query = '''
        mutation {
            updateEventDetail(
                eventId: "%s",
                phone: "%s",
                aboutEvent: "Admin updated description",
                startDate: "2024-01-03 10:00:00"
            ) {
                success
                message
            }
        }
        ''' % (self.event.id, self.admin.phone)

        response = self.client.execute(query)
        data = response.get("data", {}).get("updateEventDetail", {})

        # بررسی موفقیت‌آمیز بودن عملیات
        self.assertTrue(data["success"], "Admin should be able to update allowed fields.")
        self.assertEqual(data["message"], "Event updated successfully by the admin.")

        # بررسی تغییرات ایونت
        self.event.refresh_from_db()
        self.assertEqual(self.event.about_event, "Admin updated description", "About event should be updated.")
        self.assertEqual(str(self.event.start_date), "2024-01-03 10:00:00+00:00", "Start date should be updated.")

    def test_update_event_by_other_user(self):
        # کوئری برای به‌روزرسانی ایونت توسط کاربری که مالک یا ادمین نیست
        query = '''
        mutation {
            updateEventDetail(
                eventId: "%s",
                phone: "%s",
                aboutEvent: "Unauthorized update"
            ) {
                success
                message
            }
        }
        ''' % (self.event.id, self.other_user.phone)

        response = self.client.execute(query)
        errors = response.get("errors", [])
        data = response.get("data", {}).get("updateEventDetail", {})

        # بررسی وجود خطا
        if errors:
            self.assertIn("You do not have permission to update this event.", errors[0]["message"])
        else:
            # بررسی موفقیت‌آمیز نبودن عملیات
            self.assertFalse(data["success"], "Other users should not be able to update the event.")
            self.assertEqual(data["message"], "You do not have permission to update this event.")


class TestFilteredEventsQuery(TestCase):
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
            image="event1.jpg",
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
            neighborhood="Neighborhood 2",
            image=None,
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
            neighborhood="Neighborhood 1",
            image="event3.jpg",
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

    #def test_filtered_events_by_city(self):
    #    query = '''
    #    query {
    #        filteredEvents(city: "Tehran") {
    #            title
    #            city
    #            startDate
    #        }
    #    }
    #    '''
    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("filteredEvents", [])

    #    self.assertEqual(len(events), 3, "There should be 3 events in the city.")
    #    self.assertEqual(events[0]["title"], "Event 3", "The most recent event should come first.")
    #    self.assertEqual(events[1]["title"], "Event 2", "The second event should be Event 2.")
    #    self.assertEqual(events[2]["title"], "Event 1", "The third event should be Event 1.")

    #def test_filtered_events_by_city_and_category(self):
    #    query = '''
    #    query {
    #        filteredEvents(city: "Tehran", eventCategory: "education") {
    #            title
    #            eventCategory
    #            startDate
    #        }
    #    }
    #    '''
    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("filteredEvents", [])

    #    self.assertEqual(len(events), 2, "There should be 2 events in the category 'education'.")
    #    self.assertEqual(events[0]["title"], "Event 2", "The most recent event should come first.")
    #    self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

    #def test_filtered_events_by_city_and_neighborhood(self):
    #    query = '''
    #   query {
    #        filteredEvents(city: "Tehran", neighborhood: "Neighborhood 1") {
    #            title
    #            neighborhood
    #            startDate
    #        }
    #    }
        '''
    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("filteredEvents", [])

    #    self.assertEqual(len(events), 2, "There should be 2 events in 'Neighborhood 1'.")
    #    self.assertEqual(events[0]["title"], "Event 3", "The most recent event should come first.")
    #    self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

    #def test_filtered_events_with_images(self):
    #    query = '''
    #    query {
    #        filteredEvents(city: "Tehran", hasImage: true) {
    #            title
    #            image
    #            startDate
    #        }
    #    }
    #    '''
    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("filteredEvents", [])

    #    self.assertEqual(len(events), 2, "There should be 2 events with images.")
    #    self.assertEqual(events[0]["title"], "Event 3", "The most recent event should come first.")
    #    self.assertEqual(events[1]["title"], "Event 1", "The second event should be Event 1.")

    #def test_filtered_events_by_all_filters(self):
    #    query = '''
    #    query {
    #        filteredEvents(
    #            city: "Tehran",
    #            eventCategory: "education",
    #            neighborhood: "Neighborhood 1",
    #            hasImage: true
    #        ) {
    #            title
    #            city
    #            eventCategory
    #            neighborhood
    #            image
    #            startDate
    #        }
    #    }
    #    '''
    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("filteredEvents", [])

    #    self.assertEqual(len(events), 1, "There should be 1 event matching all filters.")
    #   self.assertEqual(events[0]["title"], "Event 1", "The event should be Event 1.")
    #    self.assertEqual(events[0]["city"], "Tehran", "City should match.")
    #    self.assertEqual(events[0]["eventCategory"], "EDUCATION", "Category should match.")
    #    self.assertEqual(events[0]["neighborhood"], "Neighborhood 1", "Neighborhood should match.")
    #    self.assertIsNotNone(events[0]["image"], "Image should not be null or empty.")


class TestRequestJoinEvent(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت ایونت تستی
        cls.event = Event.objects.create(
            title="Test Event",
            event_category="education",
            about_event="This is a test event.",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            registration_start_date="2023-12-20 10:00:00",
            registration_end_date="2023-12-30 18:00:00",
            full_description="This is the full description of the test event.",
            max_subscribers=100,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    #def test_request_join_event(self):
    #    query = '''
    #    mutation {
    #        requestJoinEvent(eventId: "%s", phone: "%s") {
    #            success
    #            message
    #        }
    #    }
    #    ''' % (self.event.id, self.user.phone)

    #    response = self.client.execute(query)
    #    data = response.get("data", {}).get("requestJoinEvent", {})

    #    self.assertTrue(data["success"], "Request to join event should be successful.")
    #    self.assertEqual(data["message"], "Request to join the event has been sent successfully.")

        # بررسی اینکه درخواست ذخیره شده است
    #    user_event_role = UserEventRole.objects.get(user=self.user, event=self.event)
    #    self.assertIsNone(user_event_role.is_approved, "User request should be pending.")
    #    self.assertEqual(user_event_role.role, "regular", "Default role should be 'regular'.")

    #def test_request_join_event_already_requested(self):
    #    # ثبت درخواست اول
    #    UserEventRole.objects.create(user=self.user, event=self.event, role="regular", is_approved=None)

        # ارسال درخواست دوباره
    #    query = '''
    #    mutation {
    #        requestJoinEvent(eventId: "%s", phone: "%s") {
    #            success
    #            message
    #        }
    #    }
    #    ''' % (self.event.id, self.user.phone)

    #    response = self.client.execute(query)
    #    data = response.get("data", {}).get("requestJoinEvent", {})

    #    self.assertFalse(data["success"], "Second request to join should fail.")
    #    self.assertEqual(data["message"], "You have already requested to join this event.")


class TestReviewJoinRequest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربران تستی
        cls.owner = User.objects.create_user(
            phone="09123456789",
            password="ownerpassword"
        )

        cls.user = User.objects.create_user(
            phone="09123456788",
            password="userpassword"
        )

        # ساخت ایونت تستی
        cls.event = Event.objects.create(
            title="Test Event",
            event_category="education",
            about_event="This is a test event.",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            registration_start_date="2023-12-20 10:00:00",
            registration_end_date="2023-12-30 18:00:00",
            full_description="This is the full description of the test event.",
            max_subscribers=100,
            event_owner=cls.owner
        )

        # ایجاد درخواست کاربر
        UserEventRole.objects.create(user=cls.user, event=cls.event, role="regular", is_approved=None)

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_approve_join_request(self):
        query = '''
        mutation {
            reviewJoinRequest(
                eventId: "%s",
                userId: "%s",
                action: "approve",
                role: "admin",
                ownerPhone: "%s"
            ) {
                success
                message
            }
        }
        ''' % (self.event.id, self.user.id, self.owner.phone)

        response = self.client.execute(query)
        data = response.get("data", {}).get("reviewJoinRequest", {})

        self.assertTrue(data["success"], "Join request approval should be successful.")
        self.assertEqual(data["message"], "User request approved successfully with role 'admin'.")

        # بررسی اینکه درخواست تایید شده است
        user_event_role = UserEventRole.objects.get(user=self.user, event=self.event)
        self.assertTrue(user_event_role.is_approved, "Join request should be approved.")
        self.assertEqual(user_event_role.role, "admin", "Role should be set to 'admin'.")

    #def test_reject_join_request(self):
    #    query = '''
    #    mutation {
    #        reviewJoinRequest(
    #            eventId: "%s",
    #            userId: "%s",
    #            action: "reject",
    #            ownerPhone: "%s"
    #        ) {
    #            success
    #            message
    #        }
    #    }
    #    ''' % (self.event.id, self.user.id, self.owner.phone)

    #    response = self.client.execute(query)
    #    data = response.get("data", {}).get("reviewJoinRequest", {})

    #    self.assertTrue(data["success"], "Join request rejection should be successful.")
    #    self.assertEqual(data["message"], "User request rejected successfully.")

        # بررسی اینکه درخواست رد شده است
    #    user_event_role = UserEventRole.objects.get(user=self.user, event=self.event)
    #    self.assertFalse(user_event_role.is_approved, "Join request should be rejected.")

    def test_invalid_action(self):
        query = '''
        mutation {
            reviewJoinRequest(
                eventId: "%s",
                userId: "%s",
                action: "invalid",
                ownerPhone: "%s"
            ) {
                success
                message
            }
        }
        ''' % (self.event.id, self.user.id, self.owner.phone)

        response = self.client.execute(query)
        data = response.get("data", {}).get("reviewJoinRequest", {})

        self.assertFalse(data["success"], "Invalid action should fail.")
        self.assertEqual(data["message"], "Invalid action provided.")


class TestCheckJoinRequestStatus(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربران تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="userpassword"
        )

        # ساخت ایونت تستی
        cls.event = Event.objects.create(
            title="Test Event",
            event_category="education",
            about_event="This is a test event.",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            registration_start_date="2023-12-20 10:00:00",
            registration_end_date="2023-12-30 18:00:00",
            full_description="This is the full description of the test event.",
            max_subscribers=100,
            event_owner=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_pending_request(self):
        UserEventRole.objects.create(user=self.user, event=self.event, is_approved=None, role="regular")

        query = '''
        query {
            checkJoinRequestStatus(phone: "09123456789", eventId: "%s") {
                message
            }
        }
        ''' % self.event.id

        response = self.client.execute(query)
        message = response.get("data", {}).get("checkJoinRequestStatus", {}).get("message", "")

        self.assertEqual(message, "Your request is pending review.")

    def test_rejected_request(self):
        UserEventRole.objects.create(user=self.user, event=self.event, is_approved=False, role="regular")

        query = '''
        query {
            checkJoinRequestStatus(phone: "09123456789", eventId: "%s") {
                message
            }
        }
        ''' % self.event.id

        response = self.client.execute(query)
        message = response.get("data", {}).get("checkJoinRequestStatus", {}).get("message", "")

        self.assertEqual(message, "Your request has been rejected.")

    def test_approved_as_regular_user(self):
        UserEventRole.objects.create(user=self.user, event=self.event, is_approved=True, role="regular")

        query = '''
        query {
            checkJoinRequestStatus(phone: "09123456789", eventId: "%s") {
                message
            }
        }
        ''' % self.event.id

        response = self.client.execute(query)
        message = response.get("data", {}).get("checkJoinRequestStatus", {}).get("message", "")

        self.assertEqual(message, "Your request has been approved as a regular user.")

    def test_approved_as_admin_user(self):
        UserEventRole.objects.create(user=self.user, event=self.event, is_approved=True, role="admin")

        query = '''
        query {
            checkJoinRequestStatus(phone: "09123456789", eventId: "%s") {
                message
            }
        }
        ''' % self.event.id

        response = self.client.execute(query)
        message = response.get("data", {}).get("checkJoinRequestStatus", {}).get("message", "")

        self.assertEqual(message, "Your request has been approved as an admin user.")

    def test_no_request_found(self):
        query = '''
        query {
            checkJoinRequestStatus(phone: "09123456789", eventId: "9999") {
                message
            }
        }
        '''

        response = self.client.execute(query)
        message = response.get("data", {}).get("checkJoinRequestStatus", {}).get("message", "")

        self.assertEqual(message, "No join request found for this event.")


class TestDeleteEvent(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.owner = User.objects.create_user(
            phone="09123456789",
            password="ownerpassword"
        )

        cls.other_user = User.objects.create_user(
            phone="09123456788",
            password="otherpassword"
        )

        # ساخت ایونت تستی
        cls.event = Event.objects.create(
            title="Test Event",
            event_category="education",
            about_event="This is a test event.",
            start_date="2024-01-01 10:00:00",
            end_date="2024-01-05 18:00:00",
            registration_start_date="2023-12-20 10:00:00",
            registration_end_date="2023-12-30 18:00:00",
            full_description="This is the full description of the test event.",
            max_subscribers=100,
            event_owner=cls.owner
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_delete_event_by_owner(self):
        query = '''
        mutation {
            deleteEvent(eventId: "%s", ownerPhone: "%s") {
                success
                message
            }
        }
        ''' % (self.event.id, self.owner.phone)

        response = self.client.execute(query)
        data = response.get("data", {}).get("deleteEvent", {})

        self.assertTrue(data["success"], "Owner should be able to delete the event.")
        self.assertEqual(data["message"], "Event deleted successfully.")

        # بررسی اینکه رویداد حذف شده است
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=self.event.id)

    def test_delete_event_by_other_user(self):
        query = '''
        mutation {
            deleteEvent(eventId: "%s", ownerPhone: "%s") {
                success
                message
            }
        }
        ''' % (self.event.id, self.other_user.phone)

        response = self.client.execute(query)
        errors = response.get("errors", [])
        data = response.get("data", {}).get("deleteEvent", {})

        # بررسی وجود خطا در پاسخ
        if errors:
            self.assertIn("You are not authorized to delete this event.", errors[0]["message"])
        else:
            self.assertFalse(data["success"], "Other users should not be able to delete the event.")
            self.assertEqual(data["message"], "You are not authorized to delete this event.")

        # بررسی اینکه رویداد همچنان وجود دارد
        self.assertTrue(Event.objects.filter(id=self.event.id).exists(), "Event should not be deleted by other users.")

    def test_delete_non_existent_event(self):
        query = '''
        mutation {
            deleteEvent(eventId: "9999", ownerPhone: "%s") {
                success
                message
            }
        }
        ''' % self.owner.phone

        response = self.client.execute(query)
        data = response.get("data", {}).get("deleteEvent", {})

        self.assertFalse(data["success"], "Deleting a non-existent event should fail.")
        self.assertEqual(data["message"], "Event not found.")


class TestEventsByOwnerQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.owner = User.objects.create_user(
            phone="09123456789",
            password="ownerpassword"
        )

        cls.other_user = User.objects.create_user(
            phone="09123456788",
            password="otherpassword"
        )

        # ساخت رویدادهای تستی
        Event.objects.create(
            title="Event 1",
            event_category="education",
            start_date="2024-12-22T10:00:00",
            end_date="2024-12-22T18:00:00",
            city="تهران",
            max_subscribers=100,
            event_owner=cls.owner
        )
        Event.objects.create(
            title="Event 2",
            event_category="sport",
            start_date="2024-12-23T15:00:00",
            end_date="2024-12-23T20:00:00",
            city="کرج",
            max_subscribers=50,
            event_owner=cls.owner
        )
        Event.objects.create(
            title="Event 3",
            event_category="music",
            start_date="2024-12-24T18:00:00",
            end_date="2024-12-24T21:00:00",
            city="اصفهان",
            max_subscribers=30,
            event_owner=cls.other_user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_events_by_owner_query(self):
        query = '''
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
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("eventsByOwner", [])

        # بررسی تعداد رویدادها
        self.assertEqual(len(events), 2, "There should be 2 events for the owner.")

        # بررسی اطلاعات رویدادها
        self.assertEqual(events[0]["title"], "Event 2", "The first event title should match.")
        self.assertEqual(events[0]["eventCategory"], "SPORT", "The first event category should match.")
        self.assertEqual(events[0]["city"], "کرج", "The first event city should match.")

        self.assertEqual(events[1]["title"], "Event 1", "The second event title should match.")
        self.assertEqual(events[1]["eventCategory"], "EDUCATION", "The second event category should match.")
        self.assertEqual(events[1]["city"], "تهران", "The second event city should match.")

    def test_events_by_owner_no_events(self):
        query = '''
        query {
            eventsByOwner(phone: "09111234567") {
                id
                title
                eventCategory
                startDate
                endDate
                city
                maxSubscribers
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("eventsByOwner", [])

        # بررسی اینکه هیچ رویدادی یافت نشده است
        self.assertEqual(len(events), 0, "There should be no events for a non-existent owner.")


from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import Event, User, UserEventRole


class TestUserEventsQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="userpassword"
        )

        cls.other_user = User.objects.create_user(
            phone="09123456788",
            password="otherpassword"
        )

        # ساخت ایونت‌های تستی
        cls.event1 = Event.objects.create(
            title="Event 1",
            event_category="education",
            start_date="2024-12-22T10:00:00",
            end_date="2024-12-22T18:00:00",
            city="تهران",
            max_subscribers=100,
            event_owner=cls.other_user
        )

        cls.event2 = Event.objects.create(
            title="Event 2",
            event_category="sport",
            start_date="2024-12-23T15:00:00",
            end_date="2024-12-23T20:00:00",
            city="کرج",
            max_subscribers=50,
            event_owner=cls.other_user
        )

        cls.event3 = Event.objects.create(
            title="Event 3",
            event_category="music",
            start_date="2024-12-24T18:00:00",
            end_date="2024-12-24T21:00:00",
            city="اصفهان",
            max_subscribers=30,
            event_owner=cls.other_user
        )

        # تنظیم روابط کاربر با رویدادها
        UserEventRole.objects.create(user=cls.user, event=cls.event1, is_approved=True, role="regular")
        UserEventRole.objects.create(user=cls.user, event=cls.event2, is_approved=True, role="regular")
        UserEventRole.objects.create(user=cls.user, event=cls.event3, is_approved=False, role="regular")

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    #def test_user_events_query(self):
    #    query = '''
    #    query {
    #       userEvents(phone: "09123456789") {
    #            id
    #            title
    #           eventCategory
    #            startDate
    #            endDate
    #            city
    #            maxSubscribers
    #        }
    #    }
    #    '''

    #    response = self.client.execute(query)
    #    events = response.get("data", {}).get("userEvents", [])

        # بررسی تعداد رویدادها
    #    self.assertEqual(len(events), 2, "There should be 2 approved events for the user.")

        # بررسی اطلاعات رویدادها
    #    self.assertEqual(events[0]["title"], "Event 2", "The first event title should match.")
    #    self.assertEqual(events[0]["eventCategory"], "SPORT", "The first event category should match.")
    #    self.assertEqual(events[0]["city"], "کرج", "The first event city should match.")

    #    self.assertEqual(events[1]["title"], "Event 1", "The second event title should match.")
    #    self.assertEqual(events[1]["eventCategory"], "EDUCATION", "The second event category should match.")
    #    self.assertEqual(events[1]["city"], "تهران", "The second event city should match.")

    def test_user_events_no_events(self):
        query = '''
        query {
            userEvents(phone: "09111234567") {
                id
                title
                eventCategory
                startDate
                endDate
                city
                maxSubscribers
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("userEvents", [])

        # بررسی اینکه هیچ رویدادی یافت نشده است
        self.assertEqual(len(events), 0, "There should be no events for a non-existent user.")


class TestAdminEventsQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="userpassword"
        )

        cls.other_user = User.objects.create_user(
            phone="09123456788",
            password="otherpassword"
        )

        # ساخت ایونت‌های تستی
        cls.event1 = Event.objects.create(
            title="Admin Event 1",
            event_category="education",
            start_date="2024-12-22T10:00:00",
            end_date="2024-12-22T18:00:00",
            city="تهران",
            max_subscribers=100,
            event_owner=cls.other_user
        )

        cls.event2 = Event.objects.create(
            title="Admin Event 2",
            event_category="sport",
            start_date="2024-12-23T15:00:00",
            end_date="2024-12-23T20:00:00",
            city="کرج",
            max_subscribers=50,
            event_owner=cls.other_user
        )

        cls.event3 = Event.objects.create(
            title="Regular Event",
            event_category="game",
            start_date="2024-12-24T18:00:00",
            end_date="2024-12-24T21:00:00",
            city="اصفهان",
            max_subscribers=30,
            event_owner=cls.other_user
        )

        # تنظیم روابط کاربر با رویدادها
        UserEventRole.objects.create(user=cls.user, event=cls.event1, is_approved=True, role="admin")
        UserEventRole.objects.create(user=cls.user, event=cls.event2, is_approved=True, role="admin")
        UserEventRole.objects.create(user=cls.user, event=cls.event3, is_approved=True, role="regular")

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_admin_events_query(self):
        query = '''
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
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("adminEvents", [])

        # بررسی تعداد رویدادها
        self.assertEqual(len(events), 2, "There should be 2 admin events for the user.")

        # بررسی اطلاعات رویدادها
        self.assertEqual(events[0]["title"], "Admin Event 2", "The first admin event title should match.")
        self.assertEqual(events[0]["eventCategory"], "SPORT", "The first admin event category should match.")
        self.assertEqual(events[0]["city"], "کرج", "The first admin event city should match.")

        self.assertEqual(events[1]["title"], "Admin Event 1", "The second admin event title should match.")
        self.assertEqual(events[1]["eventCategory"], "EDUCATION", "The second admin event category should match.")
        self.assertEqual(events[1]["city"], "تهران", "The second admin event city should match.")

    def test_admin_events_no_events(self):
        query = '''
        query {
            adminEvents(phone: "09111234567") {
                id
                title
                eventCategory
                startDate
                endDate
                city
                maxSubscribers
            }
        }
        '''

        response = self.client.execute(query)
        events = response.get("data", {}).get("adminEvents", [])

        # بررسی اینکه هیچ رویدادی یافت نشده است
        self.assertEqual(len(events), 0, "There should be no admin events for a non-existent user.")