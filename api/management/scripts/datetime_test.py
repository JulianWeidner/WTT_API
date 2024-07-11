from datetime import datetime
from django.utils.timezone import make_aware
import os, sys, django

sys.path.append('/Users/julianweidner/Development/DRF/wtt_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtt_api.settings')
django.setup()

from api.models import Tournament


example = {
"start_date_time": "2024-07-10T18:50:00Z",
"end_date_time": "2024-07-11T18:50:00Z" }

user_input = "13/07 - 15/07"


def user_input_dt_convert(u_input):
    u_input_seperated = u_input.split("-")
    u_converted_dates = []
    for list_date in u_input_seperated:
        date = list_date.strip()
        try:
            dt_str = date + "/" + str(datetime.now().year)
            split_token = "/"  
        except Exception as e:
            print('Error Converting User Input to DateTime Object' )
        u_converted_dates.append(make_aware(datetime.strptime(dt_str, f"%d{split_token}%m{split_token}%Y")))
        
        
    return u_converted_dates


    
    
u_input_dates = user_input_dt_convert(user_input)



t = Tournament.objects.filter(start_date_time__gte=u_input_dates[0], end_date_time__lte=u_input_dates[1])
print(t)






#ts = Tournament.objects.filter(start_date_time_gte=u_input_dates[0])









