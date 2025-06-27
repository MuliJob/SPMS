from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, Project, Student, Supervisor, Announcement, Proposal, Lecturer, Notification


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'is_active', 'is_staff')


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = "Student Info"

class SupervisorInline(admin.StackedInline):
    model = Supervisor
    can_delete = False
    verbose_name_plural = "Supervisor Info"

class LecturerInline(admin.StackedInline):
    model = Lecturer
    can_delete = False
    verbose_name_plural = "Lecturer Info"



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [StudentInline, SupervisorInline, LecturerInline]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role"),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically create role-specific model instance after user creation.
        """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new:
            if obj.role == "student" and not hasattr(obj, "student"):
                Student.objects.create(user=obj, registration_number=f"REG-{obj.id}")
            elif obj.role == "supervisor" and not hasattr(obj, "supervisor"):
                Supervisor.objects.create(user=obj)
            elif obj.role == "lecturer" and not hasattr(obj, "lecturer"):
                Lecturer.objects.create(user=obj)




admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Project)
admin.site.register(Announcement)
admin.site.register(Proposal)
admin.site.register(Lecturer)
admin.site.register(Notification)

