from django.db import models
from userapp.models import User


class FAQ(models.Model):
    question_title = models.CharField(max_length=255, verbose_name="عنوان سوال")
    question_answer = models.TextField(verbose_name="جواب سوال")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ایجاد کننده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ تغییر")

    class Meta:
        verbose_name = "پرسش متداول"
        verbose_name_plural = "پرسش‌های متداول"

    def __str__(self):
        return self.question_title


class Ticket(models.Model):
    # انتخاب‌های اهمیت و وضعیت
    PRIORITY_CHOICES = [
        ('high', 'زیاد'),
        ('medium', 'متوسط'),
        ('low', 'کم'),
    ]

    STATUS_CHOICES = [
        ('waiting', 'منتظر پاسخ'),
        ('answered', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    ]

    # انتخاب‌های دپارتمان
    DEPARTMENT_CHOICES = [
        ('technical', 'دپارتمان فنی'),
        ('financial', 'دپارتمان مالی'),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان تیکت")
    content = models.TextField(verbose_name="متن تیکت")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, verbose_name="دپارتمان تیکت")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="اهمیت تیکت")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name="وضعیت تیکت")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ایجاد کننده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ تغییر")

    class Meta:
        verbose_name = "تیکت پشتیبانی"
        verbose_name_plural = "تیکت‌های پشتیبانی"

    def __str__(self):
        return f"{self.title} - {self.created_by.fullname}"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE, verbose_name="تیکت مربوطه")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام تیکت"
        verbose_name_plural = "پیام‌های تیکت"

    def __str__(self):
        return f"پیام از {self.user.fullname} برای تیکت: {self.ticket.title}"


class ContactUs(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی", null=False, default='No Name')
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255, verbose_name="عنوان")
    message = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "تماس"
        verbose_name_plural = "تماس‌ها"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class Notice(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان اطلاعیه")
    content = models.TextField(verbose_name="متن اطلاعیه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد اطلاعیه")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ آپدیت اطلاعیه")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر سازنده اطلاعیه", related_name="notices")
    expiration_date = models.DateTimeField(verbose_name="تاریخ انقضای اطلاعیه")

    class Meta:
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"

    def __str__(self):
        return f"{self.title} - {self.content[:50]} - {self.expiration_date}"