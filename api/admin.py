from django.contrib import admin
from .models import (
    Profile, 
    ConnectedAccount, 
    Category, 
    Question, 
    Answer, 
    Subscription, 
    Coupon, 
    Note
)

admin.site.register(Profile)
admin.site.register(ConnectedAccount)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Note)
