from django.contrib import admin
from .models import (
    Profile, 
    Category, 
    GrammarContent, 
    Answer, 
    Subscription, 
    Coupon, 
    Note
)

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(GrammarContent)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Note)
