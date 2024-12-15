import graphene
from .mutations import RegisterUser, VerifyOTP, LoginUser, RequestLoginOTP, VerifyLoginOTP
from userapp.models import User
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)  # حذف فیلد password


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, phone=graphene.String(required=True))

    def resolve_user(self, info, phone):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    verify_otp = VerifyOTP.Field()
    login_user = LoginUser.Field()
    request_login_otp = RequestLoginOTP.Field()
    verify_login_otp = VerifyLoginOTP.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
