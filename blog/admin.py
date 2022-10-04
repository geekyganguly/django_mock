from django.contrib import admin

from blog.models import Blog 


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created')
    autocomplete_fields = ('user',)
    search_fields = ('title', 'user__first_name', 'user__last_name', 'user__mobile', 'user__email')
