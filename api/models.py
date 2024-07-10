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
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    details = models.OneToOneField('TournamentDetail', on_delete=models.CASCADE, null=True, blank=True, related_name='tournament')
    #elimination type

    
    class Meta():
        ordering = ['start_date_time']
        verbose_name = 'tournaments'

    def __str__(self):
        return self.name #should def have detail id

class TournamentDetail(models.Model):
    detail_id = models.IntegerField(unique=True)
    prize_pool = models.IntegerField()
    maps = models.JSONField()
    vehicles = models.JSONField()

    def __str__(self):
        return str(self.detail_id)
        
    
        