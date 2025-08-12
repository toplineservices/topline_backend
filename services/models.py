from django.db import models

class ServiceModels(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    
class ContactUs(models.Model):
    
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField()
    service = models.ForeignKey(ServiceModels,on_delete=models.CASCADE,related_name="contact")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)