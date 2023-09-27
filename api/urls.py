from rest_framework import routers
from django.conf import settings
from django.urls import path
from api import views
import importlib
import re
from django.db import models

router = routers.DefaultRouter()
mod = importlib.import_module("api.models")

for klassName in dir(mod):
    if "__" in klassName:
        continue
    if klassName == "models":
        continue
    klass = getattr(mod, klassName)
    if not isinstance(klass, type):  # Check if klass is a class
        continue
    if not issubclass(klass, models.Model):  # Check if klass is a subclass of models.Model
        continue
    parts = re.findall("[A-Z][^A-Z]*", klassName)
    router.register(r"%s" % "/".join(parts).lower(), views.getViewSet(klass))
urlpatterns = router.urls