import graphene
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from .models import Event, Review, Comment, EventFeature, UserEventRole
from userapp.models import User
import random


class EventType(DjangoObjectType):
    subscriber_count = graphene.Int()  # اضافه کردن فیلد subscriber_count به صورت دستی

    class Meta:
        model = Event

    def resolve_subscriber_count(self, info):
        # برگرداندن تعداد مشترکین از تعداد مرتبطین با فیلد subscribers
        return self.subscribers.count()


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ('id', 'event', 'user', 'rating', 'comment_text', 'created_at')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'review', 'user', 'comment_text', 'created_at', 'level', 'is_active')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'phone', 'fullname')


class EventDetailType(DjangoObjectType):
    class Meta:
        model = Event
        fields = '__all__'

    event_owner = graphene.Field(UserType)
    event_category = graphene.String()

    def resolve_event_owner(self, info):
        return self.event_owner

    def resolve_event_category(self, info):
        return self.event_category


class EventDetailResponseType(graphene.ObjectType):
    event = graphene.Field(EventDetailType)
    error = graphene.String()


class Query(graphene.ObjectType):
    search_events_by_city = graphene.List(EventType, city=graphene.String(required=True))
    recent_events = graphene.List(EventType)
    reviews_by_event = graphene.List(ReviewType, event_id=graphene.ID(required=True))
    comments_by_review = graphene.List(CommentType, review_id=graphene.ID(required=True))
    event_details = graphene.Field(EventDetailResponseType, event_id=graphene.ID(required=True))
    related_events = graphene.List(EventType, event_id=graphene.ID(required=True))
    events_by_city_and_category = graphene.List(EventType, city=graphene.String(required=True),
                                                category=graphene.String(required=True))
    events_by_city_and_neighborhood = graphene.List(EventType, city=graphene.String(required=True),
                                                    neighborhood=graphene.String(required=True))
    events_with_images_by_city = graphene.List(EventType, city=graphene.String(required=True))

    def resolve_search_events_by_city(self, info, city):
        return Event.objects.filter(city=city).order_by('-start_date')

    def resolve_recent_events(self, info):
        return Event.objects.annotate(subscriber_count=Count('subscribers')).order_by('-start_date', '-id')[:10]

    def resolve_reviews_by_event(self, info, event_id):
        return Review.objects.filter(event_id=event_id).order_by('-created_at')

    def resolve_comments_by_review(self, info, review_id):
        return Comment.objects.filter(review_id=review_id).order_by('-created_at')

    def resolve_event_details(self, info, event_id):
        try:
            event = Event.objects.get(id=event_id)
            return EventDetailResponseType(event=event, error=None)
        except Event.DoesNotExist:
            return EventDetailResponseType(event=None, error="Event does not exist!")

    def resolve_related_events(self, info, event_id):
        try:
            # پیدا کردن ایونت اصلی
            main_event = Event.objects.get(id=event_id)

            # فیلتر کردن ایونت‌های مرتبط با همان دسته‌بندی
            related_events = Event.objects.filter(
                event_category=main_event.event_category
            ).exclude(id=main_event.id)

            # انتخاب تصادفی ۵ ایونت از بین موارد مرتبط
            related_events = random.sample(list(related_events), min(len(related_events), 5))

            return related_events
        except Event.DoesNotExist:
            return []

    def resolve_events_by_city_and_category(self, info, city, category):
        return Event.objects.filter(city=city, event_category=category).order_by('-start_date')

    def resolve_events_by_city_and_neighborhood(self, info, city, neighborhood):
        return Event.objects.filter(city=city, neighborhood=neighborhood).order_by('-start_date')

    def resolve_events_with_images_by_city(self, info, city):
        return Event.objects.filter(city=city).exclude(image__isnull=True).exclude(image="").order_by('-start_date')


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


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = '__all__'


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'


class CreateReview(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        rating = graphene.Float(required=True)  # تغییر از Int به Float
        comment_text = graphene.String(required=True)

    review = graphene.Field(ReviewType)

    def mutate(self, info, event_id, user_id, rating, comment_text):
        # اطمینان از اینکه مقدار rating بین 0 و 5 است
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")

        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=user_id)

        review = Review.objects.create(
            event=event,
            user=user,
            rating=rating,  # ذخیره به صورت اعشاری در مدل
            comment_text=comment_text
        )

        return CreateReview(review=review)


class CreateComment(graphene.Mutation):
    class Arguments:
        review_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        comment_text = graphene.String(required=True)
        parent_comment_id = graphene.ID()  # برای ریپلای به یک کامنت (اختیاری)
        is_active = graphene.Boolean(default_value=True)  # فیلد جدید برای فعال بودن یا نبودن کامنت

    comment = graphene.Field(CommentType)

    def mutate(self, info, review_id, user_id, comment_text, parent_comment_id=None, is_active=True):
        review = Review.objects.get(id=review_id)
        user = User.objects.get(id=user_id)

        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)
            comment = Comment.objects.create(
                review=review,
                user=user,
                comment_text=comment_text,
                parent_comment=parent_comment,
                level=parent_comment.level + 1,
                is_active=is_active
            )
        else:
            comment = Comment.objects.create(
                review=review,
                user=user,
                comment_text=comment_text,
                level=1,  # اولین سطح کامنت
                is_active=is_active
            )

        return CreateComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    create_review = CreateReview.Field()
    create_comment = CreateComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
