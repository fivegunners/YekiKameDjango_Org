import graphene
from .mutations import RegisterUser, VerifyOTP, LoginUser, RequestLoginOTP, VerifyLoginOTP


class UserQuery(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, world!")


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    verify_otp = VerifyOTP.Field()
    login_user = LoginUser.Field()
    request_login_otp = RequestLoginOTP.Field()
    verify_login_otp = VerifyLoginOTP.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
