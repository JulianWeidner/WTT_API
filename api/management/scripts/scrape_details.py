from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
import django
from datetime import datetime
import time

#this is adding the DRF application program infromation to the script. Allowing the imports of tournament. etc.
sys.path.append('/Users/julianweidner/Development/DRF/wtt_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtt_api.settings')
django.setup()

from api.models import Tournament, TournamentDetail
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

def setup_driver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument('start-maximized')  #
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")

    # Set path to chromedriver as needed
    service = Service(executable_path='/Users/julianweidner/chromedriver/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def create_t_detail_obj(driver):
    t_details = Tournament.objects.values_list('detail_id', flat = True)
    
    for detail_id in t_details:
        url = f'https://tss.warthunder.com/index.php?action=tournament&id={detail_id}'
        driver.get(url)

        prize_pool_txt = driver.find_element(By.CSS_SELECTOR, 'b[id-tss="prize_pool"]').text
        try:
            prize_pool = int(prize_pool_txt.split(" ")[0])
        except Exception as e:
            print(f"detail_id:{detail_id}\ntext:{prize_pool_txt}\n{e}")

    #map function
        maps_list = []
        maps = driver.find_elements(By.NAME, 'name_maps')
        for map_element in maps:
            maps_list.append(map_element.text)
            #nation & vehicle function
            nation_vehicles = {} 
            #grab the vehicle data row (contains country flag & vehicles)
            vehicle_row_elements = driver.find_elements(By.CSS_SELECTOR, 'div.row.vehicle[name="tehnicks_flag"]')

        for row in vehicle_row_elements:
            #yoink country name from the flag image.. smh ik.
            nation_img_url = row.find_element(By.CSS_SELECTOR, 'img[name="image_flag"]').get_attribute('src')
            if nation_img_url: 
                nation_png_str = nation_img_url.split('country')[-1]
                nation = nation_png_str.split('_')[1]
                #from the same row, collect all the vehicles
                vehicles = row.find_elements(By.CSS_SELECTOR, 'div[name="tehnicks_flag"] name_netch[name="name_netch"]')
                vehicle_list = []

                for vehicle in vehicles: #clean up some of the ugly text
                    vehicle_list.append(vehicle.text.replace("▄", "").replace("▀", "").replace("◊", "").replace("◄", "").replace("␗", "").replace("▅", "")) #These just exist. Just remove them too
                nation_vehicles[f'{nation}'] = vehicle_list
    
        data = {
            'detail_id': detail_id,
            'prize_pool': prize_pool,
            'maps': maps_list,
            'vehicles': nation_vehicles
        }

        tournament_detail = TournamentDetail(**data)
        tournament_detail.save()

        linked_tournament = Tournament.objects.get(detail_id=detail_id)
        linked_tournament.details = tournament_detail
        linked_tournament.save()


        #{'id': 20059,
        #  'prize_pool': '3000 Golden eagles',
        #  'maps': ['[Conquest 2] Normandy', '[Conquest 4] Advance to the Rhine', '[Conquest 2] Sinai', ''],
        #  'nation_vehicles': {'usa': [...], 'germany': [...], 'ussr': [...], 'britain': [...], 'japan': [...], 'france': [...], 'italy': [...], 'china': [...], 'sweden': [...]}}


    return data

def main():
    driver = setup_driver()
    create_t_detail_obj(driver)
    driver.quit()


if __name__ ==  '__main__':
    main()