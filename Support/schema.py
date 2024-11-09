import graphene
from graphene_django.types import DjangoObjectType
from .models import FAQ

class FAQType(DjangoObjectType):
    class Meta:
        model = FAQ
        fields = ('question_title', 'question_answer')

class Query(graphene.ObjectType):
    all_faqs = graphene.List(FAQType)

    def resolve_all_faqs(root, info):
        return FAQ.objects.all()

schema = graphene.Schema(query=Query)