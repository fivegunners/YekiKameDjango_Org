import graphene
from .mutations import RegisterUser, VerifyOTP, LoginUser, RequestLoginOTP, VerifyLoginOTP, UpdateEmailMutation, UpdateFullnameMutation, UpdatePasswordMutation
from userapp.models import User
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
import uuid
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)  # حذف فیلد password


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, phone=graphene.String(required=True))
    check_token = graphene.String(phone=graphene.String(required=True), user_id=graphene.Int(required=True))

    def resolve_user(self, info, phone):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

    def resolve_check_token(self, info, phone, user_id):
        try:
            # بررسی وجود کاربر
            user = User.objects.get(phone=phone, id=user_id)

            # بررسی session
            sessions = Session.objects.all()
            for session in sessions:
                session_data = session.get_decoded()
                if session_data.get('user_id') == user_id and session_data.get('phone') == phone:
                    return "Token is valid."
            return "You need to login."
        except User.DoesNotExist:
            return "You need to login."


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    verify_otp = VerifyOTP.Field()
    login_user = LoginUser.Field()
    request_login_otp = RequestLoginOTP.Field()
    verify_login_otp = VerifyLoginOTP.Field()
    update_email = UpdateEmailMutation.Field()
    update_fullname = UpdateFullnameMutation.Field()
    update_password = UpdatePasswordMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
