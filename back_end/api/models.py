from django.db import models

# Create your models here.

class Convo(models.Model):
    message = models.CharField(max_length=20000)
    
    
    def __str__(self):
        return self.message
    
    