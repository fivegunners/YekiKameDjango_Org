from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import FAQ
from userapp.models import User
from datetime import datetime


class FAQQueryTest(TestCase):
    def setUp(self):
        # ایجاد یک کاربر نمونه بر اساس مدل جدید User
        self.user = User.objects.create_user(phone="09123456789", password="password123")

        # ایجاد چند FAQ نمونه
        FAQ.objects.create(question_title="What is GraphQL?", question_answer="A query language for APIs.", created_by=self.user, created_at=datetime.now())
        FAQ.objects.create(question_title="What is Django?", question_answer="A high-level Python web framework.", created_by=self.user, created_at=datetime.now())

        # تنظیم کلاینت برای اجرای کوئری‌ها
        self.client = Client(schema)

    def test_all_faqs_query(self):
        # کوئری برای گرفتن question_title و question_answer از همه FAQ ها
        query = '''
        query {
            allFaqs {
                questionTitle
                questionAnswer
            }
        }
        '''
        # اجرای کوئری
        response = self.client.execute(query)

        # چک کردن پاسخ کوئری
        data = response.get("data").get("allFaqs")

        # انتظار داریم که دو FAQ در دیتابیس باشد
        self.assertEqual(len(data), 2)

        # بررسی محتوا
        self.assertEqual(data[0]["questionTitle"], "What is GraphQL?")
        self.assertEqual(data[0]["questionAnswer"], "A query language for APIs.")
        self.assertEqual(data[1]["questionTitle"], "What is Django?")
        self.assertEqual(data[1]["questionAnswer"], "A high-level Python web framework.")
