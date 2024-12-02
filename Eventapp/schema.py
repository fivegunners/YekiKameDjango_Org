import graphene
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from .models import Event
from userapp.models import User


class EventType(DjangoObjectType):
    subscriber_count = graphene.Int()  # اضافه کردن فیلد subscriber_count به صورت دستی

    class Meta:
        model = Event
        fields = (
            "id", "title", "event_category", "about_event", "start_date", "end_date",
            "city", "province", "neighborhood", "postal_address", "postal_code",
            "max_subscribers", "event_owner", "subscribers"
        )

    def resolve_subscriber_count(self, info):
        # برگرداندن تعداد مشترکین از تعداد مرتبطین با فیلد subscribers
        return self.subscribers.count()


class Query(graphene.ObjectType):
    search_events_by_city = graphene.List(EventType, city=graphene.String(required=True))
    recent_events = graphene.List(EventType)

    def resolve_search_events_by_city(self, info, city):
        return Event.objects.filter(city=city)

    def resolve_recent_events(self, info):
        return Event.objects.annotate(subscriber_count=Count('subscribers')).order_by('-id')[:20]


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        event_category = graphene.String(required=True)
        about_event = graphene.String(required=True)
        start_date = graphene.DateTime(required=True)
        end_date = graphene.DateTime(required=True)
        registration_start_date = graphene.DateTime(required=True)
        registration_end_date = graphene.DateTime(required=True)
        province = graphene.String(required=True)
        city = graphene.String(required=True)
        neighborhood = graphene.String(required=False)  # محله
        postal_address = graphene.String(required=False)  # آدرس پستی
        postal_code = graphene.String(required=False)  # کد پستی
        max_subscribers = graphene.Int(required=True)
        event_owner_phone = graphene.String(required=True)  # شماره تلفن مالک رویداد

    event = graphene.Field(EventType)

    def mutate(self, info, title, event_category, about_event, start_date, end_date,
               registration_start_date, registration_end_date, province, city,
               max_subscribers, event_owner_phone,
               neighborhood=None, postal_address=None, postal_code=None):
        # بررسی تاریخ‌های رویداد
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        if registration_end_date <= registration_start_date:
            raise ValueError("Registration end date must be after registration start date")

        # پیدا کردن مالک رویداد بر اساس شماره تلفن
        try:
            event_owner = User.objects.get(phone=event_owner_phone)
        except User.DoesNotExist:
            raise ValueError("User with this phone number does not exist")

        # ایجاد رویداد
        event = Event.objects.create(
            title=title,
            event_category=event_category,
            about_event=about_event,
            start_date=start_date,
            end_date=end_date,
            registration_start_date=registration_start_date,
            registration_end_date=registration_end_date,
            province=province,
            city=city,
            neighborhood=neighborhood,
            postal_address=postal_address,
            postal_code=postal_code,
            max_subscribers=max_subscribers,
            event_owner=event_owner,
        )

        return CreateEvent(event=event)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
