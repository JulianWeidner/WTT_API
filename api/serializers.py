from rest_framework import serializers
from .models import Tournament, TournamentDetail

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        #fields = '__all__'
        exclude = ['id']

class TournamentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentDetail
        exclude = ['id']

    