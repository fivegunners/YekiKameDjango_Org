from django.test import TestCase
from graphene.test import Client
from .schema import schema
from .models import FAQ, ContactUs, Ticket, TicketMessage, Notice
from userapp.models import User
from datetime import datetime
from django.core import mail
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta


class FAQQueryTest(TestCase):
    def setUp(self):
        # ایجاد یک کاربر نمونه بر اساس مدل جدید User
        self.user = User.objects.create_user(phone="09123456789", password="password123")

        # ایجاد چند FAQ نمونه
        FAQ.objects.create(question_title="What is GraphQL?", question_answer="A query language for APIs.",
                           created_by=self.user, created_at=datetime.now())
        FAQ.objects.create(question_title="What is Django?", question_answer="A high-level Python web framework.",
                           created_by=self.user, created_at=datetime.now())
        FAQ.objects.create(question_title="What is Postgresql?", question_answer="A Open-Source Database.",
                           created_by=self.user, created_at=datetime.now())
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
        print(response)

        # چک کردن پاسخ کوئری
        data = response.get("data").get("allFaqs")

        # انتظار داریم که دو FAQ در دیتابیس باشد
        self.assertEqual(len(data), 3)

        # بررسی محتوا
        self.assertEqual(data[0]["questionTitle"], "What is GraphQL?")
        self.assertEqual(data[0]["questionAnswer"], "A query language for APIs.")
        self.assertEqual(data[1]["questionTitle"], "What is Django?")
        self.assertEqual(data[1]["questionAnswer"], "A high-level Python web framework.")
        self.assertEqual(data[2]["questionTitle"], "What is Postgresql?")
        self.assertEqual(data[2]["questionAnswer"], "A Open-Source Database.")


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


class CreateTicketTestCase(TestCase):
    def setUp(self):

        self.client = Client(schema)
        # ایجاد یک کاربر تست
        self.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        self.user.fullname = "John Doe"
        self.user.email = "johndoe@gmail.com"
        self.user.save()

    def test_create_ticket(self):
        # داده‌هایی که برای ایجاد تیکت استفاده می‌کنیم
        mutation = '''
            mutation {
                createTicket(
                    title: "عنوان تیکت جدید",
                    content: "متن تیکت",
                    department: "technical",
                    priority: "high",
                    status: "waiting",
                    phone: "09123456789"
                ) {
                    ticket {
                        id
                        title
                        content
                        department
                        priority
                        status
                    }
                }
            }
        '''

        # ارسال درخواست GraphQL
        response = self.client.execute(mutation)
        print(response)

        ticket_data = response.get("data", {}).get("createTicket", {}).get("ticket")

        self.assertIsNotNone(ticket_data, "The createTicket mutation returned None")

        self.assertEqual(ticket_data['title'], "عنوان تیکت جدید")
        self.assertEqual(ticket_data['content'], "متن تیکت")
        self.assertEqual(ticket_data['department'], "TECHNICAL")
        self.assertEqual(ticket_data['priority'], "HIGH")
        self.assertEqual(ticket_data['status'], "WAITING")

    def tearDown(self):
        # پاکسازی داده‌ها پس از تست
        self.user.delete()


class QueryNotice(TestCase):
    def setUp(self):

        self.client = Client(schema)
        # ایجاد یک کاربر تست
        self.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        self.user.fullname = "John Doe"
        self.user.email = "johndoe@gmail.com"
        self.user.save()

        # ایجاد اطلاعیه‌های تستی
        Notice.objects.create(
            title="Active Notice 1",
            content="This is the first active notice.",
            created_by=self.user,
            expiration_date=now() + timedelta(days=2)
        )
        Notice.objects.create(
            title="Active Notice 2",
            content="This is the second active notice.",
            created_by=self.user,
            expiration_date=now() + timedelta(days=5)
        )
        Notice.objects.create(
            title="Expired Notice",
            content="This notice has already expired.",
            created_by=self.user,
            expiration_date=now() - timedelta(days=1)
        )

    def test_active_notices_query(self):
        # کوئری برای دریافت اطلاعیه‌های فعال
        query = '''
        query {
            activeNotices {
                title
                content
            }
        }
        '''

        response = self.client.execute(query)
        notices = response.get("data", {}).get("activeNotices", [])

        # بررسی تعداد اطلاعیه‌های فعال
        self.assertEqual(len(notices), 2, "There should be 2 active notices.")

        # بررسی محتوای اطلاعیه‌های فعال
        self.assertEqual(notices[0]["title"], "Active Notice 1", "The first notice title should match.")
        self.assertEqual(notices[0]["content"], "This is the first active notice.", "The first notice content should match.")
        self.assertEqual(notices[1]["title"], "Active Notice 2", "The second notice title should match.")
        self.assertEqual(notices[1]["content"], "This is the second active notice.", "The second notice content should match.")