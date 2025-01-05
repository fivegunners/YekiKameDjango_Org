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
        #print(response)

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
        #print(response)

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


class TestCreateTicketMessage(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="password123"
        )

        # ساخت تیکت تستی
        cls.ticket = Ticket.objects.create(
            title="Test Ticket",
            content="This is a test ticket.",
            department="support",
            priority="high",
            status="waiting",
            created_by=cls.user
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_create_ticket_message(self):
        # کوئری برای ایجاد پیام جدید برای تیکت
        query = '''
        mutation {
            createTicketMessage(ticketId: "%s", phone: "%s", message: "This is a test reply.") {
                ticketMessage {
                    id
                    message
                    ticket {
                        id
                        title
                        status
                    }
                    user {
                        phone
                    }
                }
            }
        }
        ''' % (self.ticket.id, self.user.phone)

        response = self.client.execute(query)
        print(response)
        ticket_message_data = response.get("data", {}).get("createTicketMessage", {}).get("ticketMessage", {})

        # بررسی اینکه پیام ایجاد شده است
        self.assertEqual(ticket_message_data["message"], "This is a test reply.", "Message content should match.")

        # بررسی اطلاعات تیکت
        self.assertEqual(ticket_message_data["ticket"]["id"], str(self.ticket.id), "Ticket ID should match.")
        self.assertEqual(ticket_message_data["ticket"]["status"], "ANSWERED", "Ticket status should be updated to 'answered'.")

        # بررسی اطلاعات کاربر
        self.assertEqual(ticket_message_data["user"]["phone"], self.user.phone, "User phone should match.")

    def test_create_ticket_message_ticket_not_found(self):
        # کوئری برای تیکتی که وجود ندارد
        query = '''
        mutation {
            createTicketMessage(ticketId: "9999", phone: "%s", message: "This is a test reply.") {
                ticketMessage {
                    id
                }
            }
        }
        ''' % self.user.phone

        response = self.client.execute(query)
        errors = response.get("errors", [])

        # بررسی وجود خطا
        self.assertTrue(errors, "There should be an error for non-existent ticket.")
        self.assertIn("Ticket not found.", errors[0]["message"], "Error message should indicate ticket not found.")

    def test_create_ticket_message_user_not_found(self):
        # کوئری برای کاربری که وجود ندارد
        query = '''
        mutation {
            createTicketMessage(ticketId: "%s", phone: "09111111111", message: "This is a test reply.") {
                ticketMessage {
                    id
                }
            }
        }
        ''' % self.ticket.id

        response = self.client.execute(query)
        errors = response.get("errors", [])

        # بررسی وجود خطا
        self.assertTrue(errors, "There should be an error for non-existent user.")
        self.assertIn("User not found.", errors[0]["message"], "Error message should indicate user not found.")


class TestUserTicketsQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربر تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="userpassword"
        )

        # ساخت تیکت‌های تستی با تاریخ‌های دستی
        Ticket.objects.create(
            title="Ticket 1",
            department="technical",
            status="waiting",
            priority="high",
            created_by=cls.user,
            created_at="2024-01-01 10:00:00"
        )
        Ticket.objects.create(
            title="Ticket 2",
            department="financial",
            status="answered",
            priority="medium",
            created_by=cls.user,
            created_at="2024-01-02 10:00:00"
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_user_tickets_query(self):
        query = '''
        query {
            userTickets(phone: "09123456789") {
                title
                department
                status
                priority
            }
        }
        '''

        response = self.client.execute(query)
        tickets = response.get("data", {}).get("userTickets", [])

        # بررسی تعداد تیکت‌ها
        self.assertEqual(len(tickets), 2, "There should be 2 tickets for the user.")

        # بررسی اطلاعات تیکت‌ها
        self.assertEqual(tickets[0]["title"], "Ticket 2", "The first ticket title should match.")
        self.assertEqual(tickets[0]["department"], "FINANCIAL", "The first ticket department should match.")
        self.assertEqual(tickets[0]["status"], "ANSWERED", "The first ticket status should match.")
        self.assertEqual(tickets[0]["priority"], "MEDIUM", "The first ticket priority should match.")

        self.assertEqual(tickets[1]["title"], "Ticket 1", "The second ticket title should match.")
        self.assertEqual(tickets[1]["department"], "TECHNICAL", "The second ticket department should match.")
        self.assertEqual(tickets[1]["status"], "WAITING", "The second ticket status should match.")
        self.assertEqual(tickets[1]["priority"], "HIGH", "The second ticket priority should match.")

    def test_user_tickets_no_user_found(self):
        query = '''
        query {
            userTickets(phone: "09111234567") {
                title
                department
                status
                priority
            }
        }
        '''

        response = self.client.execute(query)
        tickets = response.get("data", {}).get("userTickets", [])

        # بررسی اینکه هیچ تیکتی یافت نشده است
        self.assertEqual(len(tickets), 0, "There should be no tickets for a non-existent user.")


class TestTicketMessagesQuery(TestCase):
    @classmethod
    def setUpTestData(cls):
        # ساخت کاربران تستی
        cls.user = User.objects.create_user(
            phone="09123456789",
            password="userpassword",
            is_admin=False
        )

        cls.admin_user = User.objects.create_user(
            phone="09111234567",
            password="adminpassword",
            is_admin=True
        )

        # ساخت تیکت تستی
        cls.ticket = Ticket.objects.create(
            title="Test Ticket",
            department="technical",
            status="waiting",
            priority="high",
            created_by=cls.user
        )

        # ساخت پیام‌های تستی مربوط به تیکت
        TicketMessage.objects.create(
            ticket=cls.ticket,
            user=cls.user,
            message="First message",
            created_at="2024-01-01 10:00:00"
        )
        TicketMessage.objects.create(
            ticket=cls.ticket,
            user=cls.admin_user,
            message="Second message",
            created_at="2024-01-02 12:00:00"
        )

    def setUp(self):
        # ایجاد یک کلاینت GraphQL
        self.client = Client(schema)

    def test_ticket_messages_query(self):
        query = '''
        query {
            ticketMessages(ticketId: "%s") {
                id
                message
                createdAt
                user {
                    phone
                    fullname
                    isAdmin
                }
            }
        }
        ''' % self.ticket.id

        response = self.client.execute(query)
        messages = response.get("data", {}).get("ticketMessages", [])

        # بررسی تعداد پیام‌ها
        self.assertEqual(len(messages), 2, "There should be 2 messages for the ticket.")

        # بررسی اطلاعات پیام‌های کاربر معمولی
        self.assertEqual(messages[0]["message"], "First message", "The first message content should match.")
        self.assertEqual(messages[0]["user"]["phone"], "09123456789", "The first message user phone should match.")
        self.assertFalse(messages[0]["user"]["isAdmin"], "The first message user should not be an admin.")

        # بررسی اطلاعات پیام‌های کاربر ادمین
        self.assertEqual(messages[1]["message"], "Second message", "The second message content should match.")
        self.assertEqual(messages[1]["user"]["phone"], "09111234567", "The second message user phone should match.")
        self.assertTrue(messages[1]["user"]["isAdmin"], "The second message user should be an admin.")

    def test_ticket_messages_no_ticket_found(self):
        query = '''
        query {
            ticketMessages(ticketId: "9999") {
                id
                message
                createdAt
                user {
                    phone
                    fullname
                }
            }
        }
        '''

        response = self.client.execute(query)
        messages = response.get("data", {}).get("ticketMessages", [])

        # بررسی اینکه هیچ پیامی یافت نشده است
        self.assertEqual(len(messages), 0, "There should be no messages for a non-existent ticket.")