from rest_framework import serializers
from .models import Tournament, TournamentDetail

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentDetail
        fields = '__all__'

    