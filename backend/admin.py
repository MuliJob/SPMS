from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import User, Project, Student, Supervisor, Announcement, Proposal

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Project)
admin.site.register(Announcement)
admin.site.register(Proposal)
