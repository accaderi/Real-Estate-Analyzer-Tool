### Imports ###
###############

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, emit
from threading import Lock
import time
import keyboard
from collections import OrderedDict

import real_estate_general_funcs as reg
import real_estate_visual as rav
import real_estate_webscrpmod as scr
import real_estate_df as rdf
import real_estate_pdf_maker as rpd

import pandas as pd
import json
from plotly.utils import PlotlyJSONEncoder as pjson

from html2image import Html2Image
from PIL import Image

import os



### Global ###
##############

# Flask variables
app = Flask(__name__)                                                           
app.config['SECRET_KEY'] = 'secret!'                                            
async_mode = None  
thread = None    
thread_lock = Lock()                            
socketio = SocketIO(app, async_mode=async_mode)

# Make required dirs if do not exist
dirs = reg.dir_creator()

# Read titles_txt from JSON if exists
if os.path.exists(f"{dirs['main_dir']}/titles.json"):
    title_json_path = f"{dirs['main_dir']}/titles.json"
    with open(title_json_path, "r") as file:
        titles_txt = OrderedDict(json.load(file))
else:
    titles_txt = {}


# Load (dynamic) settings
if os.path.exists(f"{dirs['main_dir']}/settings.json"):
    with open(f"{dirs['main_dir']}/settings.json", "r") as file:
        settings = json.load(file)
else:
    settings = {'to_scrap': '', 'web_browser': "chromedriver.exe", 'mapbox_api': '', 'ingatlancom_user': ['', '']}

# Load df if saved
files = os.listdir(dirs['main_dir'])
for _ in files:
    if _.endswith('filtered.csv'):
        df = pd.read_csv(f"{dirs['main_dir']}/{_}")
        print(df.shape)
        break
    else:
        df = pd.DataFrame()

# Scrapping variables
webaddress = ''
search_crit = ''
no_multiple = 0
sale = 0
t = 0
mp = 0
a =0
n =0
r = 0
d = 1
country = 'DEU'

# Chorolpleth init
ChorolJson = ''

# Terminal logo printed with scramble animation once
terminal_logo_done = 0

# Variable for the print function (webpage)
to_print_df = ''

no_post = 2



### Flask SocketIO Functions ###
################################


@socketio.event
def response_handler(message):
    global terminal_logo_done
    if message == 'y' or message == 'c':
        emit('my_response', 'To be continued... now...')
    if message == 'n':
        emit('my_response', 'Never quit except now of course... Saving scrapped data though, if there was any...')
    if message == 't':
        emit('my_response', 'Do… or do not. There is no try. Except this one fo course...')
    if message == 'Something came up. Shall I continue or try again? (c/t)':
        socketio.emit('my_response', message)
    if 'y/n' in message:
        socketio.emit('my_response', message)
        print(' sent to js: ', message)
    if message == 'Cookie accept button not clicked, sorry,':
        socketio.emit('my_response', message)
        print(' sent to js: ', message)
        time.sleep(1.3)
        socketio.emit('my_response', 'Please click it and press "c" to continue ot hit "s" for stop.')
        time.sleep(1.3)
        socketio.emit('my_response', 'You can modify the search or start over or do this on another day...')
    if message == 'Terminal logo done':
        terminal_logo_done = 1
        print(message, terminal_logo_done)
    return message


@socketio.event
def my_event(message):
    global webaddress
    global sale
    global t
    global r
    global df
    
    if settings['to_scrap'] and (webaddress or search_crit):
        if webaddress:
            response_handler(message = f'Scrapping data for "{webaddress.split("/")[2]}" processed, continue? (y/n)')
        else:
            response_handler(message = f'Scrapping data for "{search_crit}" processed, continue? (y/n)')
        user_input = ''
        while(True):
            user_input = keyboard.read_key()
            response_handler(message = user_input)
            if user_input == 'y':
                break
            elif user_input == 'n':
                response_handler(message = 'allow buttons')
                return
                
        if settings['to_scrap'] == "ingatlancom":
            if webaddress:
                if 'elado+lakas' in webaddress:
                    t, sale = 0, 0
                elif 'elado+haz' in webaddress:
                    t, sale = 1, 0
                elif 'kiado+lakas' in webaddress:
                    t, sale = 0, 1
                elif 'kiado+haz' in webaddress:
                    t, sale = 1, 1
                scrap_ingatlancom = scr.generate_ingatlancom(scr.init_all, response_handler)
            else:
                scrap_ingatlancom = scr.generate_ingatlancom(scr.init_all, response_handler)

            for result in scrap_ingatlancom.generate_all_ingatlan(settings['web_browser'], settings['ingatlancom_user'][0], settings['ingatlancom_user'][1], search_crit, no_multiple, sale, t, mp, a, n, webaddress):
                if len(result) != 8:
                    if type(result) == str and 'y/n' not in result and 'c/t' not in result:
                        socketio.emit('my_response', result)    
                else:
                    pr_mod, upr_mod, ar_mod, _ = rav.modifiers(site="ingatlancom")
                    print(result)

                    df = reg.df_creator(settings['to_scrap'], result, t, r, sale, pr_mod, upr_mod, ar_mod)
                    reg.save_files(df, search_crit, settings['to_scrap'])
            
            df = rdf.df_filter(df, pr_mod, upr_mod, ar_mod).reset_index(drop=True)
            reg.save_files(df, search_crit, settings['to_scrap'], 'filtered')
            
        elif settings['to_scrap'] == "immoscout24":

            if webaddress:
                if 'wohnung-kaufen' in webaddress:
                    t, r = 0, 0
                elif 'haus-kaufen' in webaddress:
                    t, r = 1, 0
                elif 'wohnung-mieten' in webaddress:
                    t, r = 0, 1
                elif 'haus-mieten' in webaddress:
                    t, r = 1, 1
                scrap_ingatlancom = scr.generate_immoscout24(scr.init_all, response_handler)
            else:
                scrap_ingatlancom = scr.generate_immoscout24(scr.init_all, response_handler)
            for result in scrap_ingatlancom.generate_all_immo(settings['web_browser'], country, search_crit, r, t, mp, n, a, d, webaddress):
                if len(result) != 7:
                    if type(result) == str and 'y/n' not in result and 'c/t' not in result:
                        socketio.emit('my_response', result)    
                else:
                    pr_mod, upr_mod, ar_mod, _ = rav.modifiers(site="immoscout24")
                    
                    df = reg.df_creator(settings['to_scrap'], result, t, r, sale, pr_mod, upr_mod, ar_mod)
                    reg.save_files(df, search_crit, settings['to_scrap'])

            df = rdf.df_filter(df, pr_mod, upr_mod, ar_mod).reset_index(drop=True)
            reg.save_files(df, search_crit, settings['to_scrap'], 'filtered')


### Flask Functions ###
#######################


@app.route('/')                                                                 
def index():                                                    
    return render_template('index.html', nav_link_id = 'nav_home', collapse_item = 'collapseZero')


@app.route("/scrapping", methods=["GET", "POST"])
def scrapping():

    global webaddress, search_crit, settings, no_multiple
    global sale, t, mp, a, n, r, d, country
    global terminal_logo_done

    if settings['ingatlancom_user'][0]:
        ingatlancom_user = 1
    else:
        ingatlancom_user = 0

    if request.method == "POST":
        reg.delete_files(dirs['main_dir'])

        webaddress = request.form["webaddress"]
        siteRadio = request.form["btnradio"]
        mp = int(request.form["maxprice"]) if request.form["maxprice"] else 0
        a = int(request.form["minarea"]) if request.form["minarea"] else 0
        sale = int(request.form.get("salerent")) if request.form.get("salerent") else 1
        t = int(request.form.get("realestatetype")) if request.form.get("realestatetype") else 0
        n = int(request.form.get("roomnos")) if request.form.get("roomnos") else 0
        search_crit = request.form["search"]
        no_multiple = 0 if request.form.get("excDupChk") is None else 1

        print(siteRadio, "Search parameters: ", a, t, mp, n, r, d, settings['to_scrap'])
        
        country = request.form.get("country")

        if siteRadio == "ingatlancom":
            settings['to_scrap'] = "ingatlancom"
            country = 'HU'

        elif 'immo24' in siteRadio:
            settings['to_scrap'] = "immoscout24"
            if 'deu' in siteRadio:
                country = 'DEU'
                if sale == 0: r = 0
                else: r = 1

            elif 'aut' in siteRadio:
                country = 'AUT'
                r = 0

            else:
                country = 'SPA'
                r = 0

        if search_crit:
            if n == 1: pass
            elif n == 2: n +=1
            elif n == 3: n +=2
            elif n > 3: n +=3

        elif webaddress:
            if 'immobilienscout24' in webaddress:
                settings['to_scrap'] = 'immoscout24'
            elif 'ingatlan.com' in webaddress:
                settings['to_scrap'] = 'ingatlancom'
        
        with open(f"{dirs['main_dir']}/settings.json", "w") as file:
            json.dump(settings, file)

        return redirect(url_for("socketio_scramble_effect", terminal_logo_done = terminal_logo_done))

    return render_template("scrapping.html", terminal_logo_done = terminal_logo_done, ingatlancom_user = ingatlancom_user, no_post = no_post)


@app.route("/socketio_scramble_effect", methods=["GET", "POST"])
def socketio_scramble_effect():
    return render_template("socketio_scramble_effect.html", terminal_logo_done = terminal_logo_done)


@app.route("/charts", methods=["GET"])
def charts():
    global coord, ChorolJson
    if not df.empty and settings['to_scrap']:

        ch_price, ch_price_color, ch_unitpr, ch_scatter, df_heat, prior_1, prior_2 = reg.modifiers(t, r, settings['to_scrap'])
        pr_mod, upr_mod, ar_mod, o1_mod = rav.modifiers(settings['to_scrap'])

        NopropertiesAreaJson = json.dumps(rav.NopropertiesArea(df, ar_mod), cls=pjson) #rav.NopropertiesArea(df, ar_mod).write_html('templates/temp/ch_area.html', include_plotlyjs=False, full_html = False)
        NopropertiesPricesJson = json.dumps(rav.NopropertiesPrices(df, pr_mod, o1_mod, sale, r), cls=pjson)
        NopropertiesColorJson = json.dumps(rav.NopropertiesColor(df, pr_mod, o1_mod, sale, r), cls=pjson)
        Nopropertiesm2pricesJson = json.dumps(rav.Nopropertiesm2prices(df, pr_mod, o1_mod, upr_mod, sale, r), cls=pjson)
        HeatHistJson = json.dumps(rav.HeatHist(df, pr_mod, o1_mod, ar_mod, sale, r), cls=pjson)
        UnitprAreaJson = json.dumps(rav.UnitprArea(df, settings['to_scrap'], pr_mod, upr_mod, ar_mod, o1_mod, sale, r, t), cls=pjson)
        if settings['mapbox_api']:
            if os.path.exists(f"{dirs['main_dir']}/coord.json"):
                with open(f"{dirs['main_dir']}/coord.json", "r") as file:
                    cfig, _ = rav.scatterChoropleth(df, settings['mapbox_api'], country, coord = json.load(file))
            else:
                cfig, coord = rav.scatterChoropleth(df, settings['mapbox_api'], country)
                with open(f"{dirs['main_dir']}/coord.json", "w") as file:
                    json.dump(coord, file)
            ChorolJson = json.dumps(cfig, cls=pjson)
        else:
            ChorolJson = ''

        return render_template("charts.html",
                            chart_data = [NopropertiesAreaJson,
                                        NopropertiesPricesJson,
                                        NopropertiesColorJson,
                                        Nopropertiesm2pricesJson,
                                        HeatHistJson,
                                        UnitprAreaJson,
                                        ChorolJson],
                            ch_price = ch_price,
                            ch_price_color = ch_price_color,
                            ch_unitpr = ch_unitpr,
                            ch_scatter = ch_scatter,
                            df_heat = df_heat,
                            titles_txt_orig = reg.titles_text(ch_price, ch_price_color, ch_unitpr, ch_scatter, prior_1, prior_2))

    return render_template("index.html", nav_link_id = 'nav_charts', collapse_item = 'collapseThree')


@app.route("/data", methods=["GET"])
def data():
    if not df.empty and settings['to_scrap']:
        ch_price, ch_price_color, ch_unitpr, ch_scatter, df_heat, prior_1, prior_2 = reg.modifiers(t, r, settings['to_scrap'])
        pr_mod, upr_mod, ar_mod, _ = rav.modifiers(settings['to_scrap'])
        
        return render_template("data.html", df_describe_styled = rdf.df_describe_styled(df).to_html(),
                                            df_maxes_styled = rdf.df_maxes_styled(df).to_html(),
                                            df_mins_styled = rdf.df_mins_styled(df).to_html(),
                                            df_heat_maxes_styled = rdf.df_heat_maxes_styled(df, pr_mod, ar_mod, upr_mod, r, t).to_html(),
                                            df_heat_mins_styled = rdf.df_heat_mins_styled(df, pr_mod, ar_mod, upr_mod, r, t).to_html(),
                                            df_mid_styled = rdf.df_mid_styled(df, ar_mod).to_html().replace('width: 0px;', ''),
                                            prior_1 = prior_1,
                                            prior_2 = prior_2,
                                            df_heat = df_heat,
                                            titles_txt_orig = reg.titles_text(ch_price, ch_price_color, ch_unitpr, ch_scatter, prior_1, prior_2))

    return render_template("index.html", nav_link_id = 'nav_data', collapse_item = 'collapseTwo')


@app.route("/pdf_maker", methods=["GET", "POST"])
def pdf_maker():

    if not df.empty and settings['to_scrap']:
        global titles_txt
        global to_print_df
        ch_price, ch_price_color, ch_unitpr, ch_scatter, df_heat, prior_1, prior_2, = reg.modifiers(t, r, settings['to_scrap'])
        pr_mod, upr_mod, ar_mod, o1_mod = rav.modifiers(settings['to_scrap'])
        if 'chrome' in settings['web_browser']:
            hti = Html2Image(size=(1280, 3000))
        elif 'edge' in settings['web_browser']:
            hti = Html2Image(browser='edge', size=(1280, 3000))

        if not titles_txt:
            if settings['to_scrap'] == 'ingatlancom':
                data_source = 'Ingatlan.com'
                country_source = 'Hungary'
            elif settings['to_scrap'] == 'immoscout24':
                data_source = 'Immo Scout24'
                if country == 'DEU':
                    country_source = 'Germany'
                elif country == 'AUT':
                    country_source = 'Austria'
                elif country == 'SPA':
                    country_source = 'Spain'
            titles_txt = reg.titles_text(ch_price, ch_price_color, ch_unitpr, ch_scatter, prior_1, prior_2, data_source, country_source)

        if request.method == "POST":
            jsonData = request.get_json()
            files = os.listdir(dirs['png_dir'])
            if 'pg_num' in jsonData['formData']: pg_num = 1
            else: pg_num = 0
            if 'pzero_num' in jsonData['formData']: pg_num = 2
            scr_to_take = {}
            if 'df_describe' in jsonData['formData'] and 'df_describe.png' not in files: scr_to_take['df_describe'] = rdf.df_describe_styled(df).to_html()
            if 'df_maxes' in jsonData['formData'] and 'df_maxes.png' not in files: scr_to_take['df_maxes'] = rdf.df_maxes_styled(df).hide(subset=['Link'], axis=1).to_html()
            if 'df_mins' in jsonData['formData'] and 'df_mins.png' not in files: scr_to_take['df_mins'] = rdf.df_mins_styled(df).hide(subset=['Link'], axis=1).to_html()
            if 'df_heat_maxes' in jsonData['formData'] and 'df_heat_maxes.png' not in files: scr_to_take['df_heat_maxes'] = rdf.df_heat_maxes_styled(df, pr_mod, ar_mod, upr_mod, r, t).hide(subset=['Link'], axis=1).to_html()
            if 'df_heat_mins' in jsonData['formData'] and 'df_heat_mins.png' not in files: scr_to_take['df_heat_mins'] = rdf.df_heat_mins_styled(df, pr_mod, ar_mod, upr_mod, r, t).hide(subset=['Link'], axis=1).to_html()
            if 'df_mid' in jsonData['formData'] and 'df_mid.png' not in files: scr_to_take['df_mid'] = rdf.df_mid_styled(df, ar_mod).hide(subset=['Link'], axis=1).to_html().replace('width: 0px;', '')
            if 'ch_area' in jsonData['formData'] and 'ch_area.png' not in files: scr_to_take['ch_area'] = rav.NopropertiesArea(df, ar_mod)
            if 'ch_price' in jsonData['formData'] and 'ch_price.png' not in files: scr_to_take['ch_price'] = rav.NopropertiesPrices(df, pr_mod, o1_mod, sale, r)
            if 'ch_price_color' in jsonData['formData'] and 'ch_price_color.png' not in files: scr_to_take['ch_price_color'] = rav.NopropertiesColor(df, pr_mod, o1_mod, sale, r)
            if 'ch_unitpr' in jsonData['formData'] and 'ch_unitpr.png' not in files: scr_to_take['ch_unitpr'] = rav.Nopropertiesm2prices(df, pr_mod, o1_mod, upr_mod, sale, r)
            if 'ch_heathist' in jsonData['formData'] and 'ch_heathist.png' not in files: scr_to_take['ch_heathist'] = rav.HeatHist(df, pr_mod, o1_mod, ar_mod, sale, r)
            if 'ch_scatter' in jsonData['formData'] and 'ch_scatter.png' not in files: scr_to_take['ch_scatter'] = rav.UnitprArea(df, settings['to_scrap'], pr_mod, upr_mod, ar_mod, o1_mod, sale, r, t)
            if 'ch_choropleth' in jsonData['formData'] and 'ch_choropleth.png' not in files:
                if os.path.exists(f"{dirs['main_dir']}/coord.json"):
                    with open(f"{dirs['main_dir']}/coord.json", "r") as file:
                        scr_to_take['ch_choropleth'], _ = rav.scatterChoropleth(df, settings['mapbox_api'], country, coord = json.load(file))
                else:
                    scr_to_take['ch_choropleth'], coord = rav.scatterChoropleth(df, settings['mapbox_api'], country)
                    with open(f"{dirs['main_dir']}/coord.json", "w") as file:
                        json.dump(coord, file)

            for k, v in scr_to_take.items():
                if 'df' in k:
                    to_print_df = v
                    hti.screenshot(url='http://127.0.0.1:5000/to_print', save_as='scrshot.png')
                    im = Image.open("scrshot.png")
                    im.getbbox()
                    im2 = im.crop(im.getbbox())
                    im2.save(f"{dirs['png_dir']}/{k}.png")
                elif 'ch' in k:
                    if k == 'ch_choropleth': v.write_image(f"{dirs['png_dir']}/{k}.png", width=1280, height=600, scale = 1)
                    else: v.write_image(f"{dirs['png_dir']}/{k}.png", width=640, height=500, scale = 2)
            
            try:
                os.remove('scrshot.png')
            except:
                pass

            titles_txt = OrderedDict(jsonData['titles_txt'])

            with open(f"{dirs['main_dir']}/titles.json", "w") as file:
                json.dump(titles_txt, file)

            rpd.create_pdf(titles_txt, dirs['png_dir'], pg_num)

            json_data = {'response': 'OK'}

            return json_data

        return render_template("pdf_maker.html",
                            df_heat = df_heat,
                            ch_price = ch_price,
                            ch_price_color = ch_price_color,
                            ch_unitpr = ch_unitpr,
                            ch_scatter = ch_scatter,
                            ChorolJson = ChorolJson,
                            titles_txt = json.dumps(titles_txt),
                            titles_orig_txt = reg.titles_text(ch_price, ch_price_color, ch_unitpr, ch_scatter, prior_1, prior_2))
    
    return render_template("index.html", nav_link_id = 'nav_pdf', collapse_item = 'collapseFour')


@app.route("/pdf_read", methods=["GET", "POST"])
def pdf_read():
    return render_template("pdf_read.html")


@app.route("/to_print")
def to_print():
    return render_template("to_print.html", to_print_df = to_print_df)


@app.route("/settings", methods=["GET", "POST"])
def func_settings():
    if request.method == "POST":

        global settings

        settings['web_browser'] = 'msedgedriver.exe' if int(request.form.get("web_browser")) else 'chromedriver.exe'
        settings['mapbox_api'] = request.form["mapbox_api"] if request.form["mapbox_api"] else ''
        if request.form["userName"]:
            settings['ingatlancom_user'][0] = request.form["userName"]
            settings['ingatlancom_user'][1] = request.form["passWord"]
        else:
            settings['ingatlancom_user'][0] = ''
            settings['ingatlancom_user'][1] = ''
        with open(f"{dirs['main_dir']}/settings.json", "w") as file:
            json.dump(settings, file)
    return render_template("settings.html", settingsJSON = json.dumps(settings))



if __name__ == '__main__':                                                      
    socketio.run(app, debug=True) 