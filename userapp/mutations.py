import random
from django.core.cache import cache
import graphene
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
import uuid
from .models import User
from django.contrib.auth.hashers import check_password
from graphene_django.types import DjangoObjectType
from django.contrib.sessions.backends.db import SessionStore


class RegisterUser(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, phone, password):
        # ایجاد کد OTP و ذخیره آن در کش
        otp = random.randint(10000, 99999)
        cache.set(f'otp_{phone}', otp, timeout=300)  # کد OTP به مدت 5 دقیقه ذخیره می‌شود

        # ایجاد کاربر در حالت غیرفعال
        user = User(phone=phone)
        user.set_password(password)
        user.is_active = False
        user.save()

        # ارسال کد OTP به کاربر (اینجا فرضی است و باید به کمک API پیامک انجام شود)
        print(f"OTP Code: {otp}")  # فقط برای تست

        return RegisterUser(success=True)


class VerifyOTP(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        otp = graphene.Int(required=True)

    success = graphene.Boolean()
    token = graphene.String()

    def mutate(self, info, phone, otp):
        cached_otp = cache.get(f'otp_{phone}')
        if cached_otp == otp:
            try:
                user = User.objects.get(phone=phone)
                user.is_active = True  # فعال کردن کاربر
                user.save()

                # ایجاد session
                session = SessionStore()
                session['user_id'] = user.id
                session['phone'] = phone
                session.create()

                return VerifyOTP(success=True, token=session.session_key)
            except User.DoesNotExist:
                return VerifyOTP(success=False, token=None)
        return VerifyOTP(success=False, token=None)


class LoginUser(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    token = graphene.String()

    def mutate(self, info, phone, password):
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password) and user.is_active:
                # ایجاد session
                session = SessionStore()
                session['user_id'] = user.id
                session['phone'] = phone
                session.create()

                return LoginUser(success=True, token=session.session_key)
        except User.DoesNotExist:
            pass
        return LoginUser(success=False, token=None)


class RequestLoginOTP(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, phone):
        try:
            # بررسی اینکه شماره موبایل ثبت شده باشد
            user = User.objects.get(phone=phone)

            # ایجاد و ذخیره کد OTP جدید
            otp = random.randint(10000, 99999)
            cache.set(f'login_otp_{phone}', otp, timeout=300)

            # ارسال کد OTP به کاربر (اینجا فرضی است و باید به کمک API پیامک انجام شود)
            print(f"Login OTP Code: {otp}")
            return RequestLoginOTP(success=True, message="OTP sent successfully.")
        except User.DoesNotExist:
            return RequestLoginOTP(success=False, message="User with this phone number does not exist.")


class VerifyLoginOTP(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        otp = graphene.Int(required=True)

    success = graphene.Boolean()
    token = graphene.String()

    def mutate(self, info, phone, otp):
        cached_otp = cache.get(f'login_otp_{phone}')
        if cached_otp == otp:
            try:
                user = User.objects.get(phone=phone, is_active=True)

                # ایجاد session
                session = SessionStore()
                session['user_id'] = user.id
                session['phone'] = phone
                session.create()

                return VerifyLoginOTP(success=True, token=session.session_key)
            except User.DoesNotExist:
                return VerifyLoginOTP(success=False, token=None)
        return VerifyLoginOTP(success=False, token=None)


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UpdateEmailMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        email = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, phone, email):
        try:
            user = User.objects.get(phone=phone)
            user.email = email
            user.save()
            return UpdateEmailMutation(success=True, message="Email updated successfully.")
        except User.DoesNotExist:
            return UpdateEmailMutation(success=False, message="User with the provided phone number was not found.")


class UpdateFullnameMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        fullname = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, phone, fullname):
        try:
            user = User.objects.get(phone=phone)
            user.fullname = fullname
            user.save()
            return UpdateFullnameMutation(success=True, message="Fullname updated successfully.")
        except User.DoesNotExist:
            return UpdateFullnameMutation(success=False, message="User with the provided phone number was not found.")


class UpdatePasswordMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, phone, old_password, new_password):
        try:
            user = User.objects.get(phone=phone)
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return UpdatePasswordMutation(success=True, message="Password updated successfully.")
            else:
                return UpdatePasswordMutation(success=False, message="Old password is incorrect.")
        except User.DoesNotExist:
            return UpdatePasswordMutation(success=False, message="User not found.")