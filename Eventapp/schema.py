# events/schema.py

import graphene
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from .models import Event


class EventType(DjangoObjectType):
    subscriber_count = graphene.Int()  # اضافه کردن فیلد subscriber_count به صورت دستی

    class Meta:
        model = Event
        fields = ("id", "title", "event_category", "city", "subscribers")

    def resolve_subscriber_count(self, info):
        # برگرداندن تعداد مشترکین از تعداد مرتبطین با فیلد subscribers
        return self.subscribers.count()


class Query(graphene.ObjectType):
    search_events_by_city = graphene.List(EventType, city=graphene.String(required=True))
    events_tehran = graphene.List(EventType)
    events_mashhad = graphene.List(EventType)
    events_karaj = graphene.List(EventType)
    events_shiraz = graphene.List(EventType)
    events_isfahan = graphene.List(EventType)
    events_ahvaz = graphene.List(EventType)
    events_tabriz = graphene.List(EventType)
    events_kermanshah = graphene.List(EventType)
    events_qom = graphene.List(EventType)
    events_rasht = graphene.List(EventType)
    recent_events = graphene.List(EventType)

    def resolve_search_events_by_city(self, info, city):
        return Event.objects.filter(city=city)

    def resolve_events_tehran(self, info):
        return Event.objects.filter(city="تهران")

    def resolve_events_mashhad(self, info):
        return Event.objects.filter(city="مشهد")

    def resolve_events_karaj(self, info):
        return Event.objects.filter(city="کرج")

    def resolve_events_shiraz(self, info):
        return Event.objects.filter(city="شیراز")

    def resolve_events_isfahan(self, info):
        return Event.objects.filter(city="اصفهان")

    def resolve_events_ahvaz(self, info):
        return Event.objects.filter(city="اهواز")

    def resolve_events_tabriz(self, info):
        return Event.objects.filter(city="تبریز")

    def resolve_events_kermanshah(self, info):
        return Event.objects.filter(city="کرمانشاه")

    def resolve_events_qom(self, info):
        return Event.objects.filter(city="قم")

    def resolve_events_rasht(self, info):
        return Event.objects.filter(city="رشت")

    def resolve_recent_events(self, info):
        return Event.objects.annotate(subscriber_count=Count('subscribers')).order_by('-id')[:20]


schema = graphene.Schema(query=Query)
