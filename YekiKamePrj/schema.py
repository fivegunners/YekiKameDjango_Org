import graphene
import userapp.schema  # فرض می‌کنیم نام اپلیکیشن شما userapp است


class Query(userapp.schema.Query, graphene.ObjectType):
    pass


class Mutation(userapp.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
