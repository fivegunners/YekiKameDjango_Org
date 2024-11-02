# Eventapp/tests.py

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
            max_subscribers=100,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            created_by=cls.user
        )
        Event.objects.create(
            title="Event in Mashhad",
            event_category="sport",
            city="مشهد",
            max_subscribers=50,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            created_by=cls.user
        )
        Event.objects.create(
            title="Event in Shiraz",
            event_category="game",
            city="شیراز",
            max_subscribers=80,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            created_by=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_search_events_by_city(self):
        # تست کوئری برای جستجو بر اساس شهر
        query = '''
        query {
            searchEventsByCity(city: "تهران") {
                title
                eventCategory
                city
            }
        }
        '''
        response = self.client.execute(query)
        data = response.get("data").get("searchEventsByCity")

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Event in Tehran")
        self.assertEqual(data[0]["city"], "تهران")

    def test_recent_events(self):
        # تست کوئری برای دریافت رویدادهای اخیر
        query = '''
        query {
            recentEvents {
                title
                eventCategory
                subscriberCount
            }
        }
        '''
        response = self.client.execute(query)

        # اضافه کردن بررسی برای خطاها
        if "errors" in response:
            print("GraphQL Errors:", response["errors"])

        # سپس ادامه کد
        data = response.get("data", {}).get("recentEvents")

        # بررسی اینکه recentEvents داده‌ای دارد
        self.assertIsNotNone(data, "The recentEvents query returned None")

        # بررسی تعداد رویدادهای برگردانده شده
        self.assertGreaterEqual(len(data), 3)
        self.assertEqual(data[0]["title"], "Event in Shiraz")
        self.assertIn("subscriberCount", data[0])

