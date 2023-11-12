from django.contrib import admin
from .models import AppUser, Post, Project, Category, Course, Tag
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = AppUser
    search_fields = ('email', 'username', )
    ordering = ('-id',)

    list_display = ('email', 'username')
    list_filter = ('email', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )


admin.site.register(AppUser, UserAdminConfig)
admin.site.register(Post)
# admin.site.register(Comment)
admin.site.register(Project)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Tag)