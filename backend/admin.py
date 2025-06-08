from django.contrib import admin
from .models import User, Project, Student, Supervisor, Announcement, Proposal, Lecturer, Notification
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Project)
admin.site.register(Announcement)
admin.site.register(Proposal)
admin.site.register(Lecturer)
admin.site.register(Notification)