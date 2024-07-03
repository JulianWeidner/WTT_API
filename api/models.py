from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=50)
    region = models.CharField(max_length=5)
    battle_mode = models.CharField(max_length=5)
    team_size = models.CharField(max_length=6)
    detail_id = models.IntegerField(default=0)
    tournament_type = models.CharField(max_length=20)
    #elimination type
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    class Meta():
        ordering = ['start_time']
        verbose_name = 'tournaments'

    def __str__(self):
        return self.name #should def have detail id


        
    
        