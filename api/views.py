from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tournament, TournamentDetail
from .serializers import TournamentSerializer, TournamentDetailSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_options  = ['category', 'region']
        user_filters = {}

        for option in filter_options:
            value = self.request.query_params.get(option, None)
            if value is not None:
                user_filters[option] = value
            
        if user_filters:
            queryset = queryset.filter(**user_filters) #tbf, Idk what the ** is doing in this. I'm assuming it is acting as some sort of unpacker like kwargs? For another day. Just need to see it work.
        
        return queryset




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




