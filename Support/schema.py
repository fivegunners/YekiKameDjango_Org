import graphene
from graphene_django.types import DjangoObjectType
from .models import FAQ, ContactUs, Ticket, TicketMessage, Notice
from django.core.mail import send_mail
from userapp.models import User
from django.utils.timezone import now


class FAQType(DjangoObjectType):
    class Meta:
        model = FAQ
        fields = ('question_title', 'question_answer', 'created_at')


class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        fields = ('title', 'content')


class Query(graphene.ObjectType):
    all_faqs = graphene.List(FAQType)
    active_notices = graphene.List(NoticeType)

    def resolve_active_notices(self, info):
        return Notice.objects.filter(expiration_date__gt=now())

    def resolve_all_faqs(root, info):
        return FAQ.objects.all().order_by('created_at')


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


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket
        fields = "__all__"


# تعریف Mutation برای ایجاد تیکت
class CreateTicket(graphene.Mutation):
    ticket = graphene.Field(TicketType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        department = graphene.String(required=True)
        priority = graphene.String(default_value='medium')
        status = graphene.String(default_value='waiting')
        phone = graphene.String(required=True)

    def mutate(self, info, title, content, department, priority, status, phone):
        # بررسی کاربر بر اساس شماره تلفن
        created_by = User.objects.get(phone=phone)

        # ایجاد تیکت جدید
        ticket = Ticket.objects.create(
            title=title,
            content=content,
            department=department,
            priority=priority,
            status=status,
            created_by=created_by
        )

        return CreateTicket(ticket=ticket)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "phone", "fullname", "email")


class TicketMessageType(DjangoObjectType):
    class Meta:
        model = TicketMessage
        fields = "__all__"

    user = graphene.Field(UserType)

    def resolve_user(self, info):
        return self.user


class CreateTicketMessage(graphene.Mutation):
    ticket_message = graphene.Field(TicketMessageType)

    class Arguments:
        ticket_id = graphene.ID(required=True)
        phone = graphene.String(required=True)
        message = graphene.String(required=True)

    def mutate(self, info, ticket_id, phone, message):
        try:
            # بررسی تیکت موجود
            ticket = Ticket.objects.get(id=ticket_id)
            # بررسی کاربر موجود
            user = User.objects.get(phone=phone)

            # ایجاد پیام جدید برای تیکت
            ticket_message = TicketMessage.objects.create(
                ticket=ticket,
                user=user,
                message=message
            )

            # بروزرسانی وضعیت تیکت
            ticket.status = 'answered'
            ticket.save()

            return CreateTicketMessage(ticket_message=ticket_message)
        except Ticket.DoesNotExist:
            raise Exception("Ticket not found.")
        except User.DoesNotExist:
            raise Exception("User not found.")


class Mutation(graphene.ObjectType):
    create_contact_us = CreateContactUs.Field()
    create_ticket = CreateTicket.Field()
    create_ticket_message = CreateTicketMessage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)