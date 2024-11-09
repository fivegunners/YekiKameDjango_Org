from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import FAQ, ContactUs
from userapp.models import User
from datetime import datetime
from django.core import mail
from django.utils import timezone


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


class ContactUsMutationTest(TestCase):
    def setUp(self):
        # تنظیم کلاینت برای اجرای کوئری‌ها
        self.client = Client(schema)

    def test_create_contact_us_mutation(self):
        # تعریف زمان فعلی برای بررسی فیلد created_at
        current_time = timezone.now()

        # Mutation برای افزودن ContactUs جدید
        mutation = '''
        mutation {
            createContactUs(fullName: "Ali Ahmadi", email: "user@example.com", subject: "Inquiry", message: "Please contact me") {
                contact {
                    fullName
                    email
                    subject
                    message
                    createdAt
                }
            }
        }
        '''
        # اجرای Mutation
        response = self.client.execute(mutation)

        # چک کردن داده‌های بازگشتی
        contact_data = response.get("data").get("createContactUs").get("contact")
        self.assertEqual(contact_data["fullName"], "Ali Ahmadi")
        self.assertEqual(contact_data["email"], "user@example.com")
        self.assertEqual(contact_data["subject"], "Inquiry")
        self.assertEqual(contact_data["message"], "Please contact me")

        # بررسی رکورد در دیتابیس
        contact = ContactUs.objects.get(email="user@example.com")
        self.assertEqual(contact.full_name, "Ali Ahmadi")
        self.assertEqual(contact.subject, "Inquiry")
        self.assertEqual(contact.message, "Please contact me")

        # بررسی زمان created_at
        self.assertTrue(abs((contact.created_at - current_time).total_seconds()) < 5)

        # چک کردن اینکه ایمیل به درستی ارسال شده باشد
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, "Ali Ahmadi - Inquiry")
        self.assertEqual(sent_mail.body, "Please contact me")
        self.assertEqual(sent_mail.to, ["aliahmadi79sh@gmail.com"])
