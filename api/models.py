from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta():
        ordering = ['start_time']
        verbose_name = 'tournaments'


        
    
        