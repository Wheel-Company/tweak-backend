from django.contrib import admin
from .models import (
    Profile, 
    Category, 
    WritingContent, 
    Answer, 
    Subscription, 
    Coupon, 
    Note
)

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(WritingContent)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Note)
