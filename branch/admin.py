from django.contrib import admin
from .models import User,Report,Comment,Topic
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Report)
admin.site.register(Comment)