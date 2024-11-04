from django.contrib import admin

from .models import FAQ, TicketMessage, Ticket, ContactUs

# ثبت مدل‌ها در پنل ادمین
admin.site.register(FAQ)
admin.site.register(TicketMessage)
admin.site.register(Ticket)
admin.site.register(ContactUs)