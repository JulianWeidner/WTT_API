from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tournament, TournamentDetail
from .serializers import TournamentSerializer, TournamentDetailSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def retrieve(self, request, *args, **kwargs):
        detail_id = kwargs.get('detail_id')
        t = self.queryset.filter(detail_id=detail_id).first()
        serializer = self.get_serializer(t)
        return Response(serializer.data)
   

class TournamentDetailViewSet(viewsets.ModelViewSet):
    queryset = TournamentDetail.objects.all()
    serializer_class = TournamentDetailSerializer
    
    def get_object(self):
        detail_id = self.kwargs.get('detail_id')
        t = Tournament.objects.get(detail_id=detail_id)
        return t.details
        




