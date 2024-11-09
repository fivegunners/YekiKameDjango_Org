import graphene
from graphene_django.types import DjangoObjectType
from .models import FAQ, ContactUs
from django.core.mail import send_mail


class FAQType(DjangoObjectType):
    class Meta:
        model = FAQ
        fields = ('question_title', 'question_answer')


class Query(graphene.ObjectType):
    all_faqs = graphene.List(FAQType)

    def resolve_all_faqs(root, info):
        return FAQ.objects.all()


class ContactUsType(DjangoObjectType):
    class Meta:
        model = ContactUs
        fields = ('full_name', 'email', 'subject', 'message', 'created_at')


class CreateContactUs(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        email = graphene.String(required=True)
        subject = graphene.String(required=True)
        message = graphene.String(required=True)

    contact = graphene.Field(ContactUsType)

    def mutate(self, info, full_name, email, subject, message):
        # ایجاد رکورد ContactUs
        contact = ContactUs.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )

        # ارسال ایمیل به صورت خودکار
        send_mail(
            subject=f"{full_name} - {subject}",
            message=message,
            from_email="no-reply@yekikame.com",  # آدرس ایمیل فرستنده
            recipient_list=["aliahmadi79sh@gmail.com"],
            fail_silently=False,
        )

        return CreateContactUs(contact=contact)


class Mutation(graphene.ObjectType):
    create_contact_us = CreateContactUs.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)