from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import Event
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
                city
                postalAddress
                postalCode
            }
        }
        '''
        response = self.client.execute(query)
        data = response.get("data").get("searchEventsByCity")

        self.assertIsNotNone(data[0]["id"], "ID should not be None")
        self.assertNotEqual(data[0]["id"], "", "ID should not be empty")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Event in Tehran")
        self.assertEqual(data[0]["city"], "تهران")
        self.assertEqual(data[0]["postalAddress"], "تهرانپارس، خیابان ۱۷۴ غربی")
        self.assertEqual(data[0]["postalCode"], "1592634780")

    def test_recent_events(self):
        # تست کوئری برای دریافت رویدادهای اخیر
        query = '''
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
        '''
        response = self.client.execute(query)
        data = response.get("data", {}).get("recentEvents")

        # بررسی اینکه recentEvents داده‌ای دارد
        self.assertIsNotNone(data, "The recentEvents query returned None")

        # بررسی تعداد رویدادهای برگردانده شده
        self.assertGreaterEqual(len(data), 3)
        self.assertIsNotNone(data[0]["id"], "ID should not be None")
        self.assertNotEqual(data[0]["id"], "", "ID should not be empty")
        self.assertEqual(data[0]["title"], "Event in Shiraz")
        self.assertIn("subscriberCount", data[0])
        self.assertIn("postalAddress", data[0])
        self.assertIn("postalCode", data[0])

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
                    neighborhood
                    postalAddress
                    postalCode
                    maxSubscribers
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
        self.assertEqual(event_data["postalAddress"], "Some Street, Tehran")
        self.assertEqual(event_data["postalCode"], "1234567890")
        self.assertEqual(event_data["maxSubscribers"], 150)
