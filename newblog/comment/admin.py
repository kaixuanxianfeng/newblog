from django.contrib import admin
from .models import Comment
from newblog.custom_site import custom_site
from newblog.base_admin import BaseOwnerAdmin
# Register your models here.

@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','nickname','content','website','created_time')