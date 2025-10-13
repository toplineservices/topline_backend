from django.db import models
from django.utils.text import slugify

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
    
    
class Career(models.Model):
    
    JOB_TYPE_CHOICE = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    title = models.CharField(max_length=200,null=True,blank=True)
    department = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=200,choices=JOB_TYPE_CHOICE)
    description = models.TextField()
    salary = models.CharField(max_length=50)
    requirements = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

class JobApplication(models.Model):
    career = models.ForeignKey(
        'Career', 
        on_delete=models.SET_NULL,
        null=True,blank=True, 
        related_name='applications'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    youtubeUrl = models.URLField(max_length=500, blank=True, null=True)
    video_file = models.FileField(upload_to="videos/",blank=True,null=True)  # Upload directory

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    service_img = models.ImageField(upload_to='services/images') 
    event = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

class Blog(models.Model):
    title = models.CharField(max_length=355)
    excerpt = models.TextField()
    content = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/")
    slug = models.SlugField(unique=True, blank=True,max_length=355)
    published_date = models.DateField()  # date of publication
    author = models.CharField(max_length=100, default="Topline Team") 

    def save(self, *args, **kwargs):
        if not self.slug:  
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title