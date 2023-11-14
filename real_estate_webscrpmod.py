### Imports ###
###############

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.select import Select
import undetected_chromedriver as uc
import keyboard


### General functions ###
#########################

# Initialize the webdriver and get the link
def init_all(linkToScrap='https://ingatlan.com/', driverPath=r"msedgedriver.exe"):
    """Initialize the driver for selenium and open the link (linkToScrap) in the selected browser.

    Args:
        linkToScrap (str): Link to scrap
        driverPath r(str): Path to the driver(edgebrowser driver), use r string if using '\' in path. 

    Returns:
        driver (selenium wbedriver)"""

    #

    if driverPath == r"msedgedriver.exe":
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
    # Using Edgeoptins 'excludeSwitches', ['enable-logging'] in order to disable edge Error messages like:
    #   "error:fallback_task_provider.cc(124)] every renderer should have at least one task provided by a primary task provider.
    #   if a "renderer" fallback task is shown, it is a bug.
    #   if you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782."
    #   https://stackoverflow.com/questions/69919930/selenium-edge-python-errors-auto-close-edge-browser-after-test-execution
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-notifications")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=Service(driverPath), options=options)
    
    elif driverPath == r"chromedriver.exe":
        from selenium.webdriver.chrome.options import Options 
        options = Options()
        options.page_load_strategy = 'eager'
        options.add_argument("--disable-notifications")
        # options.add_experimental_option("excludeSwitches",["enable-automation"])
        driver = uc.Chrome(service=Service(driverPath), options=options)

    driver.set_window_size(1280, 1100)
    driver.set_window_position(-5, -5) 
    wait = WebDriverWait(driver, 1000)

    driver.get(linkToScrap)
    
    return driver, wait


### Scrapping Classes ###
#########################

class generate_immoscout24():
    def __init__(self,
                 init_all,
                 response_handler):
        self.init_all = init_all
        self.response_handler = response_handler


    def variables_generator_immo(self):
        prices, locations, links = [], [], [] 
        areas, rooms, halfRooms  = [], [], []
        land_area = []
        resultsPerPage = 20
        return  areas, rooms, halfRooms, prices, locations, links, land_area, resultsPerPage
    

    def click_cookies_immo(self, driver):
        try:
            driver.execute_script('''return document.querySelector("#usercentrics-root").shadowRoot.querySelector("[data-testid='uc-accept-all-button']");''').click()
        except:
            self.response_handler(message = 'Cookie accept button not clicked, sorry,')
            user_input = ''
            while(True):
                user_input = keyboard.read_key()
                self.response_handler(message = user_input)
                break
            if user_input == 'c':
                pass
            elif user_input == 's':
                driver.quit()


    def get_res_nr_and_search_click(self, driver):
        no_of_results = driver.find_element(By.CLASS_NAME, 'oss-result-count-container')
        no_of_results_text = int(no_of_results.get_attribute('textContent').split(' ')[0].replace('.', ''))
        print(no_of_results_text)
        return no_of_results, no_of_results_text
    

    def search_method(self, driver, country = 'DEU', search_crit = 'Trier', r = 0, t = 0, mp = 0, n = 1, a = 0, d = 1):
            country, search_crit, r, t, mp, n, a, d = country, search_crit, r, t, mp, n, a, d
            print('args: ', country, search_crit, r, t, mp, n, a, d)
            
            # Choose Austria from dropdown
            #
            if country == 'AUT':
                    for _ in range(2):
                        ActionChains(driver).pause(2).perform()
                        driver.execute_script("return elem = document.getElementById('oss-selected-country')").click()
                        ActionChains(driver).pause(1).perform()
                        driver.find_element(By.XPATH, "//span[contains(text(), 'Österreich')]").click()
            
            elif country == 'SPA':
                    for _ in range(2):
                        ActionChains(driver).pause(2).perform()
                        driver.execute_script("return elem = document.getElementById('oss-selected-country')").click()
                        ActionChains(driver).pause(1).perform()
                        driver.find_element(By.XPATH, "//span[contains(text(), 'Spanien')]").click()

            # Fill the input box
            # Need to use action chain and include waits to eliminate the automatic clear button
            #
            input_box = driver.find_element(By.ID, ('oss-location'))
            ActionChains(driver)\
                    .move_to_element(input_box)\
                    .pause(1)\
                    .click_and_hold()\
                    .pause(2)\
                    .send_keys(search_crit)\
                    .pause(3)\
                    .send_keys(Keys.ENTER)\
                    .perform()
            print('i am here')

            # Buy or Rent
            # r=0 Rent, r=1 Buy, r=2 Build
            # 
            if country == 'DEU':
                rent_buy = driver.find_element(By.XPATH, f"//select[@data-value='RENT']")
                rb_selected = Select(rent_buy)
                if r == 0:
                        rb_selected.select_by_index(1)
                else:
                        rb_selected.select_by_index(0)
            
            # Select real estate type
            # Using xpath and walking along the path since the select element somehow not findable easily if at all
            # t=0 Apartment, t=1 House, from t=2 other options not considered
            #
            if t > 0:
                    if country == 'DEU':
                        if r == 1:
                            real_estate_type = driver.find_element(By.ID, 'oss-real-estate-type-rent')
                        elif r == 0:
                            real_estate_type = driver.find_element(By.ID, 'oss-real-estate-type-buy')
                    else:
                            real_estate_type = driver.find_element(By.ID, 'oss-real-estate-type-international')

                    ret_selected = Select(real_estate_type)
                    ret_selected.select_by_index(t)

            # Input max price
            # in EUR
            #
            if mp:
                    max_price = driver.find_element(By.XPATH, f"//input[@id='oss-price']").send_keys(mp)

            # Select room no
            # n=1 No matter, n=2 to n=9 means from 1, 1.5, 2, 2.5, 3, 3.5, 4, or from 5 rooms
            # 
            if n > 0:
                    room_no = driver.find_element(By.XPATH, "//select[@id='oss-rooms']")
                    rn_selected = Select(room_no)
                    rn_selected.select_by_index(n)

            # Input real estate area
            # in m2
            #
            if a > 0:
                    area_from = driver.find_element(By.XPATH, f"//input[@id='oss-area']").send_keys(a)

            # Select distance from location included in searching area
            # d=1 preimeter, d=2 to d=6 1 to 5 km, d=7 10 km, d=8 15 km, d=9 20 km, d=10 50 km
            #
            if d > 1:
                    distance = driver.find_element(By.XPATH, f"//select[@id='oss-radius']")
                    d_selected = Select(distance)
                    d_selected.select_by_index(d)

            # Click the search button and no of result
            #
            ActionChains(driver).pause(2).perform()

            try:
                no_of_results, no_of_results_text = self.get_res_nr_and_search_click(driver)
            except:
                self.response_handler(message = 'Something came up. Shall I continue or try again? (c/t)')
                user_input = ''
                while(True):
                    user_input = keyboard.read_key()
                    self.response_handler(message = user_input)
                    break
                if user_input == 'c':
                    no_of_results, no_of_results_text = self.get_res_nr_and_search_click(driver)
                elif user_input == 't':
                    self.search_method(driver, country = country, search_crit = search_crit, r = r, t = t, mp = mp, n = n, a = a, d = d)
            no_of_results.click()
            return no_of_results_text


    def total_no_pages(self, no_of_results_text, resultsPerPage):
        if no_of_results_text <= resultsPerPage:
            return 1
        return (no_of_results_text // resultsPerPage) + 1

    def click_on_next(self, driver):
        driver.find_element(By.XPATH, "//div[@id='listings']//following::ul\
                                    //child::li[contains(@class, 'p-items')][last()]\
                                    //child::a").click()


    def get_raw_data_immo(self, driver):
        ActionChains(driver).pause(5).perform()
        address_price_area_rooms = driver.find_elements(By.XPATH, "//div[@class='result-list-entry__data']")
        print(address_price_area_rooms)
        titleof = address_price_area_rooms[0].text.split('\n')[0]
        link_byclass = driver.find_elements(By.XPATH, "//h2[contains(text(), titleof)]//parent::a")
        return address_price_area_rooms, link_byclass


    def append_final_lists(self, t, areas, rooms, halfRooms, prices, locations, links,
                        link_byclass, address_price_area_rooms, land_area, listings_per_actual_page):
        act_i = 0
        for i in range(listings_per_actual_page):
            raw = address_price_area_rooms[i].text.split("\n")
            # print('-------------------------------------------', raw)
            locations.append(raw[1])
            Kaufpreis = 0
            Wohnfläche = 0
            Zi = 0
            Grundstück = 0
            for _ in raw:
                if _ =='Kaufpreis' or 'miete' in _:
                    try:
                        prices.append(float(raw[raw.index(_)-1].replace('.', '').replace(' €', '').replace(',', '.')))
                        Kaufpreis += 1
                    except:
                        pass
                if _ =='Wohnfläche':
                    try:
                        areas.append(float(raw[raw.index(_)-1].replace('.', '').replace(',', '.').replace('m\u00b2', '')))
                        Wohnfläche += 1
                    except:
                        pass
                if _ =='Zi.':
                    try:
                        if ',' in raw[raw.index(_)-1]:
                            raws = raw[_-1].split(',')
                            rooms.append(int(raws[0]))
                            halfRooms.append(int(raws[1]))
                            Zi += 1
                        else:
                            rooms.append(int(raw[raw.index(_)-1]))
                            halfRooms.append(0)
                            Zi += 1
                    except:
                        pass
                if _ =='Grundstück':
                    try:
                        land_area.append(float(raw[raw.index(_)-1].replace('.', '').replace(',', '.')[:-3]))
                        Grundstück +=1
                    except:
                        pass
            if Kaufpreis == 0:
                prices.append(0)
            if Wohnfläche == 0:
                areas.append(0)
            if Zi == 0:
                rooms.append(0)
                halfRooms.append(0)
            if t > 0 and Grundstück == 0:
                land_area.append(0)
                        
            test_subj = link_byclass[i].get_attribute('href')
            if act_i == test_subj:
                continue
            else:
                act_i = test_subj
                links.append(test_subj)


    def get_data_immo(self, areas, rooms, halfRooms, prices, locations, links,
    page_still_to_go_cntr, no_of_results_text, total_pages, land_area, resultsPerPage, t, driver, wait):
        page_still_to_go_cntr = page_still_to_go_cntr
        listings_per_actual_page = resultsPerPage
        if total_pages == page_still_to_go_cntr and no_of_results_text > 100:
            try:
                print('trying click the button to whow all the results')
                driver.find_element(By.XPATH, '//*[contains(@aria-label, "Page 5")]').click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Alle Angebote anzeigen')]"))).click()
            except:
                pass
        try:
            for _ in range(page_still_to_go_cntr):
                yield f'Page still to go: {page_still_to_go_cntr}'
                if page_still_to_go_cntr == 0:
                    return areas, rooms, halfRooms, prices, locations, links, land_area
                address_price_area_rooms, link_byclass = self.get_raw_data_immo(driver)
                print(address_price_area_rooms)
                #print(len(address_price_area_rooms), len(link_byclass))
                yield 'Data from the page scrapped. Continue sorting...'
                if page_still_to_go_cntr == 1:
                    listings_per_actual_page = no_of_results_text % resultsPerPage
                self.append_final_lists(t, areas, rooms, halfRooms, prices, locations, links,
                                    link_byclass, address_price_area_rooms, land_area, listings_per_actual_page)
                page_still_to_go_cntr -= 1
                if page_still_to_go_cntr != 0:
                    yield f'Page finished sorting. Continue next page.', page_still_to_go_cntr
                    self.click_on_next(driver)
                else:
                    yield f'Scrapping finsihed. Check out the Data or Charts section.'
                    ActionChains(driver).pause(1).perform()
        except:
            self.response_handler(message = 'Something came up. Shall I continue? (y/n)')
            user_input = ''
            while(True):
                user_input = keyboard.read_key()
                self.response_handler(message = user_input)
                break
            if user_input == 'y':
                for _ in self.get_data_immo(areas, rooms, halfRooms,
                                                    prices, locations, links, page_still_to_go_cntr,
                                                    no_of_results_text, total_pages, land_area, resultsPerPage, t, driver, wait):
                    yield _
            elif user_input == 'n':
                yield areas, rooms, halfRooms, prices, locations, links, page_still_to_go_cntr
        yield areas, rooms, halfRooms, prices, locations, links, land_area, page_still_to_go_cntr
    

    def generate_all_immo(self, driverPath, country, search_crit, r, t, mp, n, a, d=1, webaddress=''):
        print('args_no1: ', country, search_crit, r, t, mp, n, a, d)
        areas, rooms, halfRooms, prices, locations, links, land_area, \
        resultsPerPage = self.variables_generator_immo()
        if webaddress:
            print('t, r ', t, r)
            driver, wait = self.init_all(linkToScrap=webaddress, driverPath=driverPath)
            try:
                no_of_results_text = int(driver.find_element(By.XPATH, "//span[@data-is24-qa='resultlist-resultCount']").text)
            except:
                self.response_handler(message = 'Something came up. Shall I continue? (y/n)')
                user_input = ''
                while(True):
                    user_input = keyboard.read_key()
                    self.response_handler(message = user_input)
                    break
                if user_input == 'y':
                    self.click_cookies_immo(driver)
                    no_of_results_text = int(driver.find_element(By.XPATH, "//span[@data-is24-qa='resultlist-resultCount']").text)
                elif user_input == 'n':
                    driver.quit()
        else:
            driver, wait = init_all(linkToScrap='https://www.immobilienscout24.de/', driverPath=driverPath)
            ActionChains(driver).pause(2).perform()
            self.click_cookies_immo(driver)
            no_of_results_text = self.search_method(driver, country, search_crit, r = r, t = t, mp = mp, n = n, a = a, d = d)
        total_pages = self.total_no_pages(no_of_results_text, resultsPerPage)
        page_still_to_go_cntr = total_pages
        for _ in self.get_data_immo(areas, rooms, halfRooms,
                                            prices, locations, links, page_still_to_go_cntr,
                                            no_of_results_text, total_pages, land_area, resultsPerPage, t, driver, wait):
            yield _

        yield areas, rooms, halfRooms, prices, locations, links, land_area



class generate_ingatlancom():
    def __init__(self,
                 init_all,
                 response_handler):
        self.init_all = init_all
        self.response_handler = response_handler


    def variables_generator(self):
        prices, unit_prices, locations, links = [], [], [], [] 
        areas, rooms, halfRooms, balconies  = [], [], [], []
        link_byclass, prices_byclass, unitPrices_byclass, location_byclass = [], [], [], [],
        areasRoomsBalconies_byclassSibl = []
        resultsPerPage = 20
        return  prices, unit_prices, locations, links, areas, rooms, halfRooms, balconies,\
                link_byclass, prices_byclass, unitPrices_byclass, location_byclass,\
                areasRoomsBalconies_byclassSibl, resultsPerPage
    

    def ClickNoMultiple(self, driver, wait):
        # This input switch has some hidden element on it as always somewhere else in the list so we need to find which one is the clickable switch.
        # No need to perform hover click would be enough too.
        # Maybe wait also would not be necessary but in some cases slow download of the page can be an issue.
        sameAdvertCheck = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[class*="m1x-switch form-check-input me-3"][data-action*="change->listings-page--main#toggleM1xSwitchValue"]')))
        
        if sameAdvertCheck[0].is_selected() == False:
            for _ in range(len(sameAdvertCheck)):  
                try:
                    hover = ActionChains(driver).move_to_element(sameAdvertCheck[_]).click().perform()
                except:
                    continue


    def clickSuti(self, wait):
        allow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Összes süti')]")))
        allow_button.click()


    def SearchMtd(self, driver, wait, search_crit, sale = 0, t = 0, mp = 0, a = 0, n = 1):
        ActionChains(driver).pause(2).perform()
        try:
            # Buy or Rent
            # 
            if sale:
                driver.find_element(By.CSS_SELECTOR, "label[for*='rent']").click()
            else:
                driver.find_element(By.CSS_SELECTOR, "label[for*='sale']").click()
            
            # Select real estate type
            # t=0 Apartment, t=1 House, from t=2 other options not considered
            #
            if t:
                real_estate_type = driver.find_element(By.CSS_SELECTOR, "[id*='propertyType']")
                ret_selected = Select(real_estate_type)
                ret_selected.select_by_index(t)

            # Input max price
            # in HUF
            #
            if mp:
                driver.find_element(By.CSS_SELECTOR, "[data-testid='price-range-to']").send_keys(mp)

            # Input real estate area
            # in m2
            #
            if a:
                driver.find_element(By.CSS_SELECTOR, "[data-testid='area-range-from']").send_keys(a)

            # Select room no
            # n=1 No matter, n=2 to n=9 means from 1, 1.5, 2, 2.5, 3, 3.5, 4, or from 5 rooms
            # 
            if n > 1:
                driver.find_element(By.CSS_SELECTOR, "[data-testid='room-range-from']").send_keys(n)

            # Fill the input box
            #
            inputWhere_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Hol keresel?"]')))
            inputWhere_click.send_keys(' ')

            inputWhere = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="pl.: V. ker vagy Szeged Ősz utca"]')))
            inputWhere.send_keys(search_crit)
            
            #ActionChains(driver).pause(5).perform()
            input1st = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="suggestion-label"]'))).click()

            okBtn = driver.find_elements(By.XPATH, "//*[contains(text(), 'Rendben')]")
            for _ in range(len(okBtn)):
                if okBtn[_].text == 'Rendben':
                    #assert okBtn[1].text == 'Rendben', f'other button: {okBtn[1].text}'
                    okBtn[_].click()
                else:
                    pass

            searchBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="button"][title*="eresés"]'))).click()
        except:
            try:
                driver.find_element(By.CSS_SELECTOR, "[id*='interstitial-close-button']").click()
            except:
                pass


    # def findLoginBtn(self, wait):
    #     try:
    #         loginBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id*='header-login-button']")))
    #     except:
    #         loginBtn=0
    #     return loginBtn


    def loginToPage(self, driver, wait, userName, passWord):
        try:
            menuBtn = driver.find_elements(By.CSS_SELECTOR, "[class*='navbar-toggler-icon']")
            menuBtn[0].click()
        except:
            pass

        loginBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id*='header-login-button']")))
        loginBtn.click()

        inputEmail = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]')))
        inputEmail.send_keys(userName)

        inputPwd = driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
        inputPwd[0].send_keys(passWord)

        submitBtn = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
        assert submitBtn[0].get_attribute('data-auth-target') == 'loginSubmitButton',\
            f'other button: {submitBtn[0].get_attribute("data-auth-target")}'
        submitBtn[0].click()


    def noOfPages_generator(self, wait, resultsPerPage):
        nrOfResults = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), ' találat')][contains(@class, 'px-0 d-block text-nickel')]")))
        real_nrOfResults = int(nrOfResults.get_attribute('textContent')[:-8].replace(' ', ''))
        if real_nrOfResults % resultsPerPage: noOfPages = (real_nrOfResults // resultsPerPage)+1
        else: noOfPages = real_nrOfResults // resultsPerPage
        return noOfPages, real_nrOfResults


    def linkPriceUnitPriceLocatareasBalc_generator(self, driver):
        elementList_dict = {'link_byclass': driver.find_elements(By.CSS_SELECTOR, "[class*='listing-card'][href*='/']"),
        'prices_byclass' : driver.find_elements(By.CLASS_NAME, 'fw-bold.fs-5.text-onyx.me-3.font-family-secondary'),
        'unitPrices_byclass' : driver.find_elements(By.CSS_SELECTOR, "[class*='fs-7 text-nickel align-self-end align-self-md-center mb-1 mb-md-0 font-family-base listing-card-area-prices']"),
        'location_byclass' : driver.find_elements(By.CSS_SELECTOR, "[class*='d-block fw-500 fs-7 text-onyx font-family-secondary']"),
        'areasRoomsBalconies_byclassSibl' : driver.find_elements(By.XPATH, "//span[@class='fs-8 text-nickel font-family-secondary']//following-sibling::span")}
        
        for index, value in elementList_dict.items():
            elementList_dict[index] = [element for element in value if element.is_displayed()]

        return elementList_dict


    def areasRoomsBalconies_generator(self, areas, rooms, halfRooms, balconies, areasRoomsBalconies_byclassSibl):
        areasRoomsBalconies_text = [txt.text for txt in areasRoomsBalconies_byclassSibl]

        for nr in range(len(areasRoomsBalconies_text)):

            if 'm' in areasRoomsBalconies_text[nr]:        
                try:
                    areasRoomsBalconies_text[nr+1]
                    if 'm' in areasRoomsBalconies_text[nr+1]:
                        if len(balconies):
                            balconies.pop(-1)
                        balconies.append(float(areasRoomsBalconies_text[nr][:-3]))
                        continue

                except IndexError:
                    if len(balconies):
                        balconies.pop(-1)
                    balconies.append(float(areasRoomsBalconies_text[nr][:-3]))
                    break
                areas.append(float(areasRoomsBalconies_text[nr][:-3]))
                balconies.append(0)

            elif 'fél' in areasRoomsBalconies_text[nr]:
                if '+' in areasRoomsBalconies_text[nr]:
                    rooms.append(int(areasRoomsBalconies_text[nr][:-4].split(' + ')[0]))
                    halfRooms.append(int(areasRoomsBalconies_text[nr][:-4].split(' + ')[1]))
                else:
                    halfRooms.append(int(areasRoomsBalconies_text[nr][:-4]))
                    rooms.append(0)

            else:
                rooms.append(int(areasRoomsBalconies_text[nr]))
                halfRooms.append(0)
                
        return areas, rooms, halfRooms, balconies
    

    def pricesUnitpricesLocationsLinks_generator(self, prices, unit_prices, locations, links, elementList_dict, sale):
        prices.extend([float(price.text[:-5].replace(',', '.')) if 'M Ft' in price.text else float(price.text[:-6].replace(' ', '')) for price in elementList_dict['prices_byclass']])
        unit_prices.extend([float(price.text[:-8].replace(' ', '')) for price in elementList_dict['unitPrices_byclass']])
            
        # location can be divided to district, address maybe the hous nr. is separate too.
        locations.extend([location.text for location in elementList_dict['location_byclass']])
        
        links.extend([link.get_attribute('href') for link in elementList_dict['link_byclass']])
        
        return prices, unit_prices, locations, links
    

    def clickForward(self, driver, wait):
        # driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });") # scroll to the end of the page
        driver.execute_script("window.scrollBy(horizontal_scroll = 0 , vertical_scroll = 10000 );") # scrolling to the bottom of the page 3rd option
        forward_arrow = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='list']/div[2]/div[1]/div[4]/div[3]/a")))
        if len(forward_arrow) > 1:
                # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END) # scroll to the end of the page 2nd option
                while True:
                    try:
                        # forward_arrow[0].click()
                        forward_arrow[0].get_attribute('href')
                        driver.get(forward_arrow[0].get_attribute('href'))
                    except:
                        try:
                            forward_arrow[1].get_attribute('href')
                            driver.get(forward_arrow[0].get_attribute('href'))
                        except ElementClickInterceptedException:
                            bt = driver.find_elements(By.CSS_SELECTOR, "[class*='material-icons me-2 text-gray fs-6 fw-bold text-decoration-none'][role='button']")
                            btn = [t for t in bt if t.text == 'close'][0].click()
                            continue
                        break
                    break
        forward_arrow[0].get_attribute('href')
        driver.get(forward_arrow[0].get_attribute('href'))


    def add_click_away(self, driver):
        driver.find_element(By.XPATH, "//*[@id='interstitial-close-button']").click()


    def get_data_ingatlan(self, areas, rooms, halfRooms, balconies, prices,
                            unit_prices, locations, links,
                            page_still_to_go_cntr, resultsPerPage, sale, driver,
                            wait):
        page_still_to_go_cntr = page_still_to_go_cntr
        try:
            for _ in range(page_still_to_go_cntr):
                yield f'Page still to go: {page_still_to_go_cntr}'
                if page_still_to_go_cntr == 0:
                    return (areas, rooms, halfRooms, balconies, prices,\
                            unit_prices, locations, links)
                elementList_dict = self.linkPriceUnitPriceLocatareasBalc_generator(driver)
                yield 'Data from the page scrapped. Continue sorting...'
                ActionChains(driver).pause(1).perform()
                areas, rooms, halfRooms, balconies = self.areasRoomsBalconies_generator(areas, rooms, halfRooms, balconies, areasRoomsBalconies_byclassSibl=elementList_dict['areasRoomsBalconies_byclassSibl'])
                prices, unit_prices, locations, links = self.pricesUnitpricesLocationsLinks_generator(prices, unit_prices, locations, links, elementList_dict, sale)
                page_still_to_go_cntr -= 1
                if page_still_to_go_cntr != 0:
                    yield f'Page finished sorting. Continue next page.'
                    self.clickForward(driver, wait)
                else:
                    yield f'Scrapping finsihed. Check out the Data or Charts section.'
                    # ActionChains(driver).pause(1).perform()
        except:
            self.response_handler(message = 'Something came up. Shall I continue? (y/n)')
            user_input = ''
            while(True):
                user_input = keyboard.read_key()
                self.response_handler(message = user_input)
                break
            if user_input == 'y':
                for _ in self.get_data_ingatlan(areas, rooms, halfRooms, balconies, prices,
                            unit_prices, locations, links,
                            page_still_to_go_cntr, resultsPerPage, sale, driver,
                            wait):
                    yield _
            elif user_input == 'n':
                yield areas, rooms, halfRooms, balconies, prices,\
                            unit_prices, locations, links,\
                            page_still_to_go_cntr
                
        yield areas, rooms, halfRooms, balconies, prices,\
                            unit_prices, locations, links,\
                            page_still_to_go_cntr


    def generate_all_ingatlan(self, driverPath, userName=0, passWord=0, search_crit='Körmend',
                              no_multiple=0, sale = 0, t = 0, mp = 0, a = 0, n = 1, webaddress=''):
        prices, unit_prices, locations, links, areas, rooms, halfRooms, balconies,\
                link_byclass, prices_byclass, unitPrices_byclass, location_byclass,\
                areasRoomsBalconies_byclassSibl, resultsPerPage  = self.variables_generator()
        yield 'Received parameters: ', no_multiple, sale, t, mp, a, n
        if webaddress:
            driver, wait = self.init_all(linkToScrap=webaddress, driverPath=driverPath)
            self.clickSuti(wait)
            # real_estate_type = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id*='propertyType']")))
            # if real_estate_type.get_attribute('value') == 'flat':
            #     t = 0
            # else:
            #     t = 1            
        else:
            driver, wait = self.init_all(linkToScrap='https://www.ingatlan.com/', driverPath=driverPath)
            try:
                ActionChains(driver).pause(3).perform()
                self.add_click_away(driver)
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, "label[for*='sale']").click()
                    pass
                except:  
                    ActionChains(driver).pause(3).perform()
            else:
                pass
            self.clickSuti(wait)
            self.SearchMtd(driver, wait, search_crit, sale = sale, t = t, mp = mp, a = a, n = n)
        if userName and passWord:
            # self.findLoginBtn(wait)
            self.loginToPage(driver, wait, userName, passWord)
        if userName and passWord and no_multiple:
            self.ClickNoMultiple(driver, wait)
        noOfPages, real_nrOfResults = self.noOfPages_generator(wait, resultsPerPage)
        page_still_to_go_cntr = noOfPages
        for _ in self.get_data_ingatlan(areas, rooms, halfRooms, balconies, prices,
                            unit_prices, locations, links,
                            page_still_to_go_cntr, resultsPerPage, sale, driver,
                            wait):
            yield _

        yield areas, rooms, halfRooms, balconies, prices, unit_prices, locations, links

