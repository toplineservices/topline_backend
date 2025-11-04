from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Admin


# --- Forms ---
class AdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ('email', 'name', 'designation')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.set_password(self.cleaned_data["password1"])
        if commit:
            admin.save()
        return admin


class AdminChangeForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('email', 'name', 'designation', 'is_active')


# --- Admin Config ---
class AdminAdmin(UserAdmin):
    add_form = AdminCreationForm
    form = AdminChangeForm
    model = Admin

    list_display = ('email', 'name', 'designation', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'designation')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'designation', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

# ✅ Register the Admin model *after* defining the class
admin.site.register(Admin, AdminAdmin)
