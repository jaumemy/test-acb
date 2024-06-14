from django.db import models

# Create your models here.


class MatchEvent(models.Model):
    """
    MatchEvents model
    Stores basic info an event in a match
    """

    game_id = models.IntegerField(verbose_name="Game ID")
    team_id = models.IntegerField(null=True, blank=True, verbose_name="Team ID")
    player_license_id = models.IntegerField(null=True, blank=True, verbose_name="Player License ID")
    action_time = models.CharField(max_length=8, null=True, blank=True, verbose_name="Action Time")
    action_type = models.SmallIntegerField(verbose_name="Action Type")
