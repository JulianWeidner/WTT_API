from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tournament, TournamentDetail
from .serializers import TournamentSerializer, TournamentDetailSerializer
from datetime import datetime
from django.utils.timezone import make_aware


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_options  = ['category', 'region']
        user_filters = {}
        #in discord a user would type //wtt land eu today-07/10 ----- //wtt air eu 07/10 - 07/20
        #timespan filter handler
        def date_span_handler(u_input):
            #u_input shoudl always be a span. I'll update this eventually to not require a span
            u_input_seperated = u_input.split("-")
       
            u_converted_dates = []
            
            for list_date in u_input_seperated:
                date = list_date.strip()
         
                try:
                    dt_str = date + "/" + str(datetime.now().year) #create a string & then split it ? lol
                    split_token = "/"  
                    aware_datetime = make_aware(datetime.strptime(dt_str, f"%d{split_token}%m{split_token}%Y"))
                    print(aware_datetime)
                    u_converted_dates.append(aware_datetime)
                except Exception as e:
                    print('Error Converting User Input to DateTime Object', e )
                    return None
            return u_converted_dates

        #check for user filters
        for option in filter_options:
            value = self.request.query_params.get(option, None)
            if value is not None:
                user_filters[option] = value
        
        if 'date_span' in self.request.query_params:
            date_span_value = self.request.query_params['date_span']
            date_range = date_span_handler(date_span_value)
        
            if date_range:
                queryset = queryset.filter(start_date_time__gte=date_range[0], end_date_time__lte=date_range[1])


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




