from django.contrib import admin   
from .models import FoodPost, Request

admin.site.register(FoodPost)
admin.site.register(Request)