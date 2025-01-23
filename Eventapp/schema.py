import graphene
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from .models import Event, Review, Comment, EventFeature, UserEventRole
from userapp.models import User
import random
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from graphene_file_upload.scalars import Upload
from django.utils import timezone

class EventType(DjangoObjectType):
    subscriber_count = graphene.Int()

    class Meta:
        model = Event

    def resolve_subscriber_count(self, info):
        # شمارش کاربران تایید شده به علاوه owner
        approved_count = UserEventRole.objects.filter(
            event=self,
            is_approved=True
        ).count()
        
        # اگر owner در subscribers نیست، یک نفر اضافه می‌کنیم
        owner_is_subscriber = UserEventRole.objects.filter(
            event=self,
            user=self.event_owner
        ).exists()
        
        if not owner_is_subscriber:
            approved_count += 1
            
        return approved_count

class PastEventType(DjangoObjectType):
    role = graphene.String()

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_date', 'end_date', 'event_category', 'neighborhood', 'city')
        convert_choices_to_enum = False
    def resolve_role(self, info):
        context = info.context
        try:
            # ابتدا بررسی می‌کنیم که آیا کاربر owner است
            if self.event_owner.phone == context.phone:
                return "owner"
            
            # اگر owner نبود، سایر نقش‌ها را بررسی می‌کنیم
            user_role = UserEventRole.objects.get(
                event=self,
                user__phone=context.phone
            )
            return user_role.role  # می‌تواند "admin" یا "regular" باشد
            
        except UserEventRole.DoesNotExist:
            return None

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
    subscriber_count = graphene.Int()

    def resolve_event_owner(self, info):
        return self.event_owner

    def resolve_event_category(self, info):
        return self.event_category

    def resolve_subscriber_count(self, info):
        return self.subscribers.count()  # محاسبه تعداد subscribers

class JoinRequestType(DjangoObjectType):
    user = graphene.Field(UserType)
    created_at = graphene.DateTime()

    class Meta:
        model = UserEventRole
        fields = ('id', 'role', 'is_approved', 'created_at')

    def resolve_user(self, info):
        return self.user

class EventDetailResponseType(graphene.ObjectType):
    event = graphene.Field(EventDetailType)
    error = graphene.String()


class UserEventRoleType(DjangoObjectType):
    event = graphene.Field(EventType)
    user = graphene.Field(UserType)

    class Meta:
        model = UserEventRole
        fields = ('id', 'role', 'is_approved')


class CheckJoinRequestStatus(graphene.ObjectType):
    message = graphene.String()

    class Arguments:
        phone = graphene.String(required=True)
        event_id = graphene.ID(required=True)

    def resolve(self, info, phone, event_id):
        try:
            # بررسی وجود رابطه کاربر و رویداد
            user_event_role = UserEventRole.objects.get(
                user__phone=phone,
                event__id=event_id
            )

            if user_event_role.is_approved is None:
                return CheckJoinRequestStatus(message="Your request is pending review.")
            elif user_event_role.is_approved is False:
                return CheckJoinRequestStatus(message="Your request has been rejected.")
            elif user_event_role.is_approved is True:
                if user_event_role.role == "regular":
                    return CheckJoinRequestStatus(message="Your request has been approved as a regular user.")
                elif user_event_role.role == "admin":
                    return CheckJoinRequestStatus(message="Your request has been approved as an admin user.")

        except UserEventRole.DoesNotExist:
            return CheckJoinRequestStatus(message="No join request found for this event.")

class NotificationType(DjangoObjectType):
    event_title = graphene.String()
    status_message = graphene.String()
    
    class Meta:
        model = UserEventRole
        fields = ('id', 'event', 'role', 'is_approved', 'created_at')

    def resolve_event_title(self, info):
        return self.event.title

    def resolve_status_message(self, info):
        if self.is_approved is True:
            if self.role == "admin":
                return f"شما به عنوان ادمین در رویداد {self.event.title} پذیرفته شدید"
            else:
                return f"درخواست عضویت شما در رویداد {self.event.title} پذیرفته شد"
        elif self.is_approved is False:
            return f"درخواست عضویت شما در رویداد {self.event.title} رد شد"
        return None

class Query(graphene.ObjectType):
    search_events_by_city = graphene.List(EventType, city=graphene.String(required=True))
    recent_events = graphene.List(EventType)
    reviews_by_event = graphene.List(ReviewType, event_id=graphene.ID(required=True))
    comments_by_review = graphene.List(CommentType, review_id=graphene.ID(required=True))
    event_details = graphene.Field(EventDetailResponseType, event_id=graphene.ID(required=True))
    related_events = graphene.List(EventType, event_id=graphene.ID(required=True))
    filtered_events = graphene.List(
        EventType,
        city=graphene.String(required=True),
        event_category=graphene.String(),
        neighborhood=graphene.String(),
        has_image=graphene.Boolean()
    )
    check_join_request_status = graphene.Field(CheckJoinRequestStatus, phone=graphene.String(required=True),
                                               event_id=graphene.ID(required=True))
    events_by_owner = graphene.List(EventType, phone=graphene.String(required=True))
    user_events = graphene.List(EventType, phone=graphene.String(required=True))
    admin_events = graphene.List(EventType, phone=graphene.String(required=True))
    search_events_by_title = graphene.List(
        EventType,
        title=graphene.String(required=True),
        limit=graphene.Int(default_value=10) 
    )
    past_events = graphene.List(PastEventType, phone=graphene.String(required=True))
    pending_join_requests = graphene.List(
        JoinRequestType,
        event_id=graphene.ID(required=True),
        owner_phone=graphene.String(required=True)
    )
    user_notifications = graphene.List(NotificationType, phone=graphene.String(required=True))
    mark_notification_as_read = graphene.Boolean(
        user_event_role_id=graphene.ID(required=True),
        phone=graphene.String(required=True)
    )
    def resolve_admin_events(self, info, phone):
        try:
            user = User.objects.get(phone=phone)
            return Event.objects.filter(
                subscribers=user,
                usereventrole__is_approved=True,
                usereventrole__role='admin'
            ).order_by('-start_date')
        except User.DoesNotExist:
            return []

    def resolve_user_events(self, info, phone):
        try:
            if not phone:  # اگر phone خالی باشد
                return []
                
            user = User.objects.get(phone=phone)
            current_date = timezone.now()
            
            # فقط رویدادهایی که کاربر در آنها regular است
            return Event.objects.filter(
                subscribers=user,
                usereventrole__is_approved=True,
                usereventrole__role='regular',
                end_date__gte=current_date  # رویدادهای جاری و آینده
            ).order_by('-start_date')
        
        except User.DoesNotExist:
            return []

    def resolve_events_by_owner(self, info, phone):
        try:
            user = User.objects.get(phone=phone)
            return Event.objects.filter(event_owner=user).order_by('-start_date')
        except User.DoesNotExist:
            return []

    def resolve_check_join_request_status(self, info, phone, event_id):
        return CheckJoinRequestStatus().resolve(info, phone, event_id)

    def resolve_search_events_by_city(self, info, city):
        return Event.objects.filter(city=city).order_by('-start_date')

    def resolve_recent_events(self, info):
        current_date = timezone.now()
        return Event.objects.filter(
            registration_end_date__gte=current_date  # فقط رویدادهایی که هنوز تمام نشده‌اند
        ).annotate(
            subscriber_count=Count('subscribers')
        ).order_by('-start_date', '-id')[:10]

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
            current_date = timezone.now()
            main_event = Event.objects.get(id=event_id)

            related_events = Event.objects.filter(
                Q(event_category=main_event.event_category) &
                Q(city=main_event.city) &
                Q(registration_end_date__gte=current_date)  # فقط رویدادهای فعال
            ).exclude(id=main_event.id)

            related_events = random.sample(list(related_events), min(len(related_events), 5))
            return related_events
        except Event.DoesNotExist:
            return []

    def resolve_filtered_events(self, info, city, event_category=None, neighborhood=None, has_image=None):
        current_date = timezone.now()
        # فیلتر اولیه بر اساس شهر و تاریخ
        filters = Q(city=city) & Q(registration_end_date__gte=current_date)

        # افزودن فیلترهای اختیاری
        if event_category:
            filters &= Q(event_category=event_category)
        if neighborhood:
            filters &= Q(neighborhood=neighborhood)
        if has_image is not None:
            if has_image:
                filters &= ~Q(image__isnull=True) & ~Q(image="")
            else:
                filters &= Q(image__isnull=True) | Q(image="")

        return Event.objects.filter(filters).order_by('-start_date')
    def resolve_search_events_by_title(self, info, title, limit=10):
        current_date = timezone.now()

        return Event.objects.filter(
            Q(title__icontains=title) &  # جستجو در عنوان (case-insensitive)
            Q(registration_end_date__gte=current_date) 
        ).order_by('-start_date')[:limit]
    def resolve_past_events(self, info, phone):
        current_date = timezone.now()
        try:
            user = User.objects.get(phone=phone)
            
            # پیدا کردن همه رویدادهای گذشته کاربر (شامل رویدادهایی که owner است)
            past_events = Event.objects.filter(
                (
                    Q(subscribers=user) |  # رویدادهایی که کاربر در آنها عضو است
                    Q(event_owner=user)    # رویدادهایی که کاربر owner آنهاست
                ) &
                Q(end_date__lt=current_date)  # رویدادهایی که تمام شده‌اند
            ).distinct().order_by('-end_date')

            # اضافه کردن phone به context برای استفاده در resolve_role
            info.context.phone = phone
            
            return past_events

        except User.DoesNotExist:
            return []

    def resolve_pending_join_requests(self, info, event_id, owner_phone):
        try:
            # بررسی دسترسی owner
            event = Event.objects.get(id=event_id)
            owner = User.objects.get(phone=owner_phone)
            
            if event.event_owner != owner:
                raise PermissionDenied("Only the event owner can view join requests")

            # دریافت درخواست‌های در انتظار
            return UserEventRole.objects.filter(
                event_id=event_id,
                is_approved__isnull=True  # فقط درخواست‌های در انتظار
            ).order_by('created_at')  # مرتب‌سازی بر اساس زمان ثبت (قدیمی‌ترین اول)

        except (Event.DoesNotExist, User.DoesNotExist):
            return []
    def resolve_user_notifications(self, info, phone):
        try:
            user = User.objects.get(phone=phone)
            current_date = timezone.now()
            
            # دریافت درخواست‌های بررسی شده که:
            # 1. هنوز خوانده نشده‌اند
            # 2. مربوط به رویدادهای جاری یا آینده هستند
            return UserEventRole.objects.filter(
                user=user,
                is_approved__isnull=False,  # فقط درخواست‌های بررسی شده
                event__end_date__gte=current_date  # فقط رویدادهای جاری و آینده
            ).exclude(
                notificationstatus__user=user,  # حذف موارد خوانده شده
                notificationstatus__is_read=True
            ).order_by('-created_at')

        except User.DoesNotExist:
            return []

    def resolve_mark_notification_as_read(self, info, user_event_role_id, phone):
        try:
            user = User.objects.get(phone=phone)
            user_event_role = UserEventRole.objects.get(id=user_event_role_id)
            
            # ایجاد یا به‌روزرسانی وضعیت اعلان
            NotificationStatus.objects.update_or_create(
                user=user,
                user_event_role=user_event_role,
                defaults={'is_read': True}
            )
            
            return True

        except (User.DoesNotExist, UserEventRole.DoesNotExist):
            return False
class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        event_category = graphene.String(required=True)
        about_event = graphene.String(required=True)
        image = Upload(required=False)  # آپلود فایل تصویر
        start_date = graphene.DateTime(required=True)
        end_date = graphene.DateTime(required=True)
        registration_start_date = graphene.DateTime(required=True)
        registration_end_date = graphene.DateTime(required=True)
        province = graphene.String(required=True)
        city = graphene.String(required=True)
        neighborhood = graphene.String(required=False)  # محله
        postal_address = graphene.String(required=False)  # آدرس پستی
        postal_code = graphene.String(required=False)  # کد پستی
        full_description = graphene.String(required=False)  # توضیحات کامل
        max_subscribers = graphene.Int(required=True)
        event_owner_phone = graphene.String(required=True)  # شماره تلفن مالک رویداد

    event = graphene.Field(EventType)

    def mutate(self, info, title, event_category, about_event, start_date, end_date,
               registration_start_date, registration_end_date, province, city,
               max_subscribers, event_owner_phone,
               neighborhood=None, postal_address=None, postal_code=None,
               full_description=None, image=None):
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

        # ذخیره‌سازی تصویر
        image_path = None
        if image:
            image_path = f"http://localhost:8000/media/event_images/{image.name}"
            with open(image_path, "wb") as f:
                f.write(image.read())

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
            full_description=full_description,
            max_subscribers=max_subscribers,
            event_owner=event_owner,
            image=image_path,
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


class UpdateEventDetail(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        phone = graphene.String(required=True)
        title = graphene.String()
        event_category = graphene.String()
        about_event = graphene.String()
        image = graphene.String()
        start_date = graphene.DateTime()
        end_date = graphene.DateTime()
        registration_start_date = graphene.DateTime()
        registration_end_date = graphene.DateTime()
        full_description = graphene.String()
        max_subscribers = graphene.Int()
        province = graphene.String()
        city = graphene.String()
        neighborhood = graphene.String()
        postal_address = graphene.String()
        postal_code = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, event_id, phone, **kwargs):
        try:
            # پیدا کردن ایونت و کاربر
            event = Event.objects.get(id=event_id)
            user = User.objects.get(phone=phone)

            # بررسی نقش کاربر
            if event.event_owner == user:
                # اگر Owner باشد، همه فیلدها قابل ویرایش است
                for field, value in kwargs.items():
                    if value is not None:
                        setattr(event, field, value)
                event.save()
                return UpdateEventDetail(success=True, message="Event updated successfully by the owner.")

            elif UserEventRole.objects.filter(user=user, event=event, role='admin').exists():
                # اگر Admin باشد، فقط فیلدهای خاص قابل ویرایش است
                allowed_fields = [
                    'about_event', 'image', 'start_date', 'end_date',
                    'registration_start_date', 'registration_end_date',
                    'full_description', 'max_subscribers'
                ]
                for field, value in kwargs.items():
                    if field in allowed_fields and value is not None:
                        setattr(event, field, value)
                event.save()
                return UpdateEventDetail(success=True, message="Event updated successfully by the admin.")

            else:
                raise PermissionDenied("You do not have permission to update this event.")

        except Event.DoesNotExist:
            return UpdateEventDetail(success=False, message="Event not found.")
        except User.DoesNotExist:
            return UpdateEventDetail(success=False, message="User not found.")


class RequestJoinEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        phone = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, event_id, phone):
        try:
            # بررسی وجود رویداد
            event = Event.objects.get(id=event_id)
            # بررسی وجود کاربر
            user = User.objects.get(phone=phone)

            # ایجاد درخواست پیوستن
            user_event_role, created = UserEventRole.objects.get_or_create(
                user=user,
                event=event,
                defaults={"role": "regular", "is_approved": None}
            )

            if not created:
                return RequestJoinEvent(success=False, message="شما قبلا درخواست عضویت خود را ارسال کرده اید.")

            return RequestJoinEvent(success=True, message="درخواست عضویت شما با موفقیت ارسال گردید.")

        except Event.DoesNotExist:
            return RequestJoinEvent(success=False, message="رویداد پیدا نشد.")
        except User.DoesNotExist:
            return RequestJoinEvent(success=False, message="کاربر یافت نشد.")


class ReviewJoinRequest(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        action = graphene.String(required=True)  # "approve" یا "reject"
        role = graphene.String()  # "regular" یا "admin" در صورت تایید
        owner_phone = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, event_id, user_id, action, owner_phone, role=None):
        try:
            event = Event.objects.get(id=event_id)
            owner = User.objects.get(phone=owner_phone)
            if event.event_owner != owner:
                raise PermissionDenied("You are not authorized to review join requests for this event.")

            user_event_role = UserEventRole.objects.get(event=event, user_id=user_id)
            user = User.objects.get(id=user_id)

            if action == "approve":
                user_event_role.is_approved = True
                user_event_role.role = role if role in ["regular", "admin"] else "regular"
                user_event_role.save()
                
                # اضافه کردن کاربر به subscribers
                event.subscribers.add(user)
                
                return ReviewJoinRequest(success=True, message=f"User request approved successfully with role '{user_event_role.role}'.")
            elif action == "reject":
                user_event_role.is_approved = False
                user_event_role.save()
                
                # حذف کاربر از subscribers اگر قبلاً اضافه شده بود
                event.subscribers.remove(user)
                
                return ReviewJoinRequest(success=True, message="User request rejected successfully.")
            else:
                return ReviewJoinRequest(success=False, message="Invalid action provided.")

        except Event.DoesNotExist:
            return ReviewJoinRequest(success=False, message="Event not found.")
        except User.DoesNotExist:
            return ReviewJoinRequest(success=False, message="Owner not found.")
        except UserEventRole.DoesNotExist:
            return ReviewJoinRequest(success=False, message="User join request not found.")


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        owner_phone = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, event_id, owner_phone):
        try:
            # بررسی وجود رویداد
            event = Event.objects.get(id=event_id)

            # بررسی اینکه کاربر بررسی‌کننده مالک رویداد باشد
            owner = User.objects.get(phone=owner_phone)
            if event.event_owner != owner:
                raise PermissionDenied("You are not authorized to delete this event.")

            # حذف رویداد
            event.delete()
            return DeleteEvent(success=True, message="Event deleted successfully.")

        except Event.DoesNotExist:
            return DeleteEvent(success=False, message="Event not found.")
        except User.DoesNotExist:
            return DeleteEvent(success=False, message="Owner not found.")


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    create_review = CreateReview.Field()
    create_comment = CreateComment.Field()
    update_event_detail = UpdateEventDetail.Field()
    request_join_event = RequestJoinEvent.Field()
    review_join_request = ReviewJoinRequest.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
