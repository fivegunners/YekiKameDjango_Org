from django.test import TestCase
from graphene.test import Client
from django.core.cache import cache
from .schema import schema
from .models import User


class UserMutationsTest(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.phone = "09123456789"
        self.password = "testpassword"

    def test_register_user(self):
        # تست ثبت‌نام کاربر
        response = self.client.execute('''
            mutation {
                registerUser(phone: "%s", password: "%s") {
                    success
                }
            }
        ''' % (self.phone, self.password))

        self.assertTrue(response['data']['registerUser']['success'])

        # بررسی ذخیره OTP در کش
        otp = cache.get(f'otp_{self.phone}')
        self.assertIsNotNone(otp)

    def test_verify_otp(self):
        # تنظیم پیش‌شرط برای تست
        cache.set(f'otp_{self.phone}', 12345, timeout=300)
        User.objects.create(phone=self.phone, is_active=False)

        # تست تأیید OTP
        response = self.client.execute('''
            mutation {
                verifyOtp(phone: "%s", otp: 12345) {
                    success
                }
            }
        ''' % self.phone)

        self.assertTrue(response['data']['verifyOtp']['success'])

        # بررسی فعال شدن کاربر
        user = User.objects.get(phone=self.phone)
        self.assertTrue(user.is_active)

    def test_login_user(self):
        # تنظیم پیش‌شرط برای تست
        user = User(phone=self.phone)
        user.set_password(self.password)
        user.is_active = True
        user.save()

        # تست لاگین با رمز عبور
        response = self.client.execute('''
            mutation {
                loginUser(phone: "%s", password: "%s") {
                    success
                }
            }
        ''' % (self.phone, self.password))

        self.assertTrue(response['data']['loginUser']['success'])

    def test_request_login_otp(self):
        # تست درخواست OTP برای لاگین
        response = self.client.execute('''
            mutation {
                requestLoginOtp(phone: "%s") {
                    success
                }
            }
        ''' % self.phone)

        self.assertTrue(response['data']['requestLoginOtp']['success'])

        # بررسی ذخیره OTP در کش
        otp = cache.get(f'login_otp_{self.phone}')
        self.assertIsNotNone(otp)

    def test_verify_login_otp(self):
        # تنظیم پیش‌شرط برای تست
        user = User.objects.create(phone=self.phone, is_active=True)
        cache.set(f'login_otp_{self.phone}', 54321, timeout=300)

        # تست تأیید OTP برای لاگین
        response = self.client.execute('''
            mutation {
                verifyLoginOtp(phone: "%s", otp: 54321) {
                    success
                }
            }
        ''' % self.phone)

        self.assertTrue(response['data']['verifyLoginOtp']['success'])
