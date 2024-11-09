from django.db import models
from userapp.models import User


class Event(models.Model):
    Category_CHOICES = [
        ('education', 'Education'),
        ('sport', 'Sport'),
        ('game', 'Game'),
        ('entertainment', 'Entertainment'),
        ('social', 'Social'),
    ]
    title = models.CharField(max_length=255)
    event_category = models.CharField(max_length=50, choices=Category_CHOICES, default='education')
    about_event = models.TextField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    province = models.CharField(max_length=100, default='تهران')
    city = models.CharField(max_length=100, default='تهران')
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True, blank=True)  # آدرس پستی
    postal_code = models.CharField(max_length=20, null=True, blank=True)  # کد پستی
    registration_start_date = models.DateTimeField(null=True, blank=True)  # تاریخ شروع ثبت نام
    registration_end_date = models.DateTimeField(null=True, blank=True)  # تاریخ پایان ثبت نام
    full_description = models.TextField()
    max_subscribers = models.PositiveIntegerField()
    event_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    subscribers = models.ManyToManyField(User, through='UserEventRole', related_name='joined_events')

    def __str__(self):
        return f"{self.title} - {self.event_category} - {self.about_event[:15]}"

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"


class UserEventRole(models.Model):
    ROLE_CHOICES = [
        ('regular', 'Regular'),
        ('admin', 'Admin'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    is_approved = models.BooleanField(default=False)  # برای تائید یا رد کاربران

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.fullname} - {self.event.title} - {self.role}"

    class Meta:
        verbose_name = "نقش کاربر در رویداد"
        verbose_name_plural = "نقش کاربرها در رویداد"


class EventFeature(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='custom_features')
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value} for {self.event.title}"

    class Meta:
        verbose_name = "ویژگی رویداد"
        verbose_name_plural = "ویژگی های رویداد"
