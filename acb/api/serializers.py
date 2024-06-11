from rest_framework import serializers

from .models import MatchEvent


class MatchEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchEvent
        fields = (
            'team_id',
            'player_license_id',
            'action_time',
            'action_type'
        )
