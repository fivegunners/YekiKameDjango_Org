import graphene
import userapp.schema  # اضافه کردن schema اپلیکیشن userapp
import Eventapp.schema  # اضافه کردن schema اپلیکیشن Eventapp
import Support.schema  # اضافه کردن schema اپلیکیشن Support

class Query(userapp.schema.Query, Eventapp.schema.Query, Support.schema.Query, graphene.ObjectType):
    pass

class Mutation(userapp.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
