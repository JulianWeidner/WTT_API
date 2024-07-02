from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
import django

sys.path.append('/Users/julianweidner/Development/DRF/wtt_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtt_api.settings')
django.setup()

from api.models import Tournament

#from tournament import Tournament, TournamentDetail
import time

#create driver/browser open page
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

def close_gdpr(driver):
    print('closing GDPR')
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "button[data-cookiefirst-action='reject']")))
        deny_button = driver.find_element(By.CSS_SELECTOR, "button[data-cookiefirst-action='reject']")
        deny_button.click()
    except Exception as e:
        print(f'Failed to close GDPR: {str(e)}')

def get_active_tournaments(driver):
    past_card = driver.find_elements(By.CSS_SELECTOR, ".row.container_info_tournament.past")
    active_tournaments = []
    more_btn = driver.find_element(By.ID, 'linkLoadTournaments')
    #initial page load card gather

    #check for inactive cards to signify end of active cards list
    while not past_card:
        print('clicking more')
        more_btn.click()
        time.sleep(2)
        past_card = driver.find_elements(By.CSS_SELECTOR, ".row.container_info_tournament.past")
    print('found past card')
    
    #gather active_cards
    active_cards = driver.find_elements(By.CSS_SELECTOR, '.row.container_info_tournament.open')
    for card in active_cards:
        active_tournaments.append(card)
    print(f'total_tournaments: {len(active_tournaments)}')

    #figure out a proper return
    return (active_tournaments)


def create_tournament_obj(tournament_card):

    detail_id = tournament_card.find_element(By.CSS_SELECTOR, 'a[card-name="buttonInfoTournament"]').get_attribute('href').split("=")[-1]

    """
        name = models.CharField(max_length=300)
        start_time = models.DateTimeField()
        end_time = models.DateTimeField()
    """


    data = {
        'name': tournament_card.find_element(By.CSS_SELECTOR, 'h3.header-name-tournament').text,
        #'team_size': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='formatTeam']").text,
        #'registrations': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='countTeam']").text,
        #'battle_mode': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='gameMode']").text,
        #'tournament_type': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='typeTournament']").text,
        #'region': tournament_card.find_element(By.CSS_SELECTOR, "span[card-name='clusterTournament']").text,
        #'tournament_date': tournament_card.find_element(By.CSS_SELECTOR, "p[card-name='dayTournament']").text,
        'detail_id': detail_id
    }

    return Tournament(**data)

def get_tournament_details(sub_driver, tournament):
    url = f'https://tss.warthunder.com/index.php?action=tournament&id={tournament.detail_id}'
    sub_driver.get(url)

    #map function
    maps_list = []
    maps = sub_driver.find_elements(By.NAME, 'name_maps')
    for map_element in maps:
        maps_list.append(map_element.text)

    
    #nation & vehicle function
    nation_vehicles = {} #dictonary of nation: [vehicles] 
    #grab the vehicle data row (contains country flag & vehicles)
    vehicle_row_elements = sub_driver.find_elements(By.CSS_SELECTOR, 'div.row.vehicle[name="tehnicks_flag"]')

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
                vehicle_list.append(vehicle.text.replace("▄", "").replace("▀", "")) # ◊ ◄␗these just exist. Just remove them.
            nation_vehicles[f'{nation}'] = vehicle_list

    
    data = {
        'id': tournament.detail_id,
        'prize_pool':  sub_driver.find_element(By.CSS_SELECTOR, 'b[id-tss="prize_pool"]').text,
        'maps': maps_list,
        'nation_vehicles': nation_vehicles
    }

    sub_driver.quit()
    return data

def create_tournament_detail(data):
    return TournamentDetail(**data)

    

def main():
    driver = setup_driver()
    driver.get("https://tss.warthunder.com/index.php?action=current_tournaments#")
    
    #close gdpr 
    close_gdpr(driver)


    active_tournaments = get_active_tournaments(driver)


    print('Creating Tournament Objects (printed from main)')
    for tournament in active_tournaments:
        #sub_driver = setup_driver()
        tourn_obj = create_tournament_obj(tournament)
        tourn_obj.save()
        #tourn_detail_elements = get_tournament_details(sub_driver, tourn_obj)
        #tourn_detail_obj = create_tournament_detail(tourn_detail_elements)

        #print("Tournament Object:",  tourn_obj.title, tourn_obj.date), "--", tourn_detail_obj.id, tourn_detail_obj.prize_pool,#, tourn_detail_obj.prize_pool )
        #print("T Detail Object: ", tourn_detail_obj.id, tourn_detail_obj.prize_pool, tourn_detail_obj.maps, tourn_detail_obj.nation_vehicles)
    
    driver.quit()



if __name__ ==  '__main__':
    main()
