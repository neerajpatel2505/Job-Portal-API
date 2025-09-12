from django.db import models
from django.utils import timezone
# Create your models here.


class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
class Applicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_link = models.URLField()
    applied_job = models.ForeignKey(JobPost, related_name='applicants', on_delete=models.CASCADE)
    applied_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.applied_job.title}"