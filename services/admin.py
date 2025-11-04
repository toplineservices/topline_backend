from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from authentication.models import Admin

from .models import (
    ServiceModels,
    ContactUs,
    Career,
    JobApplication,
    Video,
    Gallery,
    Blog,
    SiteVisit,
    
)





admin.site.register(ServiceModels)
admin.site.register(ContactUs)
admin.site.register(Career)
admin.site.register(JobApplication)
admin.site.register(Video)
admin.site.register(Gallery)
admin.site.register(Blog)
admin.site.register(SiteVisit)
