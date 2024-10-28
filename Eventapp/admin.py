from django.contrib import admin
from . import models

admin.site.register(models.Event)
admin.site.register(models.EventFeature)
admin.site.register(models.UserEventRole)

