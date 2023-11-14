import plotly.express as px
import urllib.parse as up
import numpy as np
import requests
import re


def modifiers(site, sale = 0, r = 0):
    if site == 'ingatlancom':
        if sale or r:
            pr_mod = 'HUF/mo'
        else:
            pr_mod = 'MHUF'
        upr_mod = 'HUF/m\u00b2'
        ar_mod = 'm\u00b2'
        o1_mod = 'Million HUF'
    elif site == 'immoscout24':
        if r:
            pr_mod = 'EUR/mo'
        else:
            pr_mod = 'EUR'
        upr_mod = 'EUR/m\u00b2'
        ar_mod = 'm\u00b2'
        o1_mod = 'EUR'
    return pr_mod, upr_mod, ar_mod, o1_mod


def zoom_center(lons: tuple=None, lats: tuple=None, lonlats: tuple=None,
        format: str='lonlat', projection: str='mercator',
        width_to_height: float=2.0) -> (float, dict):
    """Finds optimal zoom and centering for a plotly mapbox.
    Must be passed (lons & lats) or lonlats.
    Temporary solution awaiting official implementation, see:
    https://github.com/plotly/plotly.js/issues/3434
    
    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    lonlats: tuple, optional, gps locations
    format: str, specifying the order of longitud and latitude dimensions,
        expected values: 'lonlat' or 'latlon', only used if passed lonlats
    projection: str, only accepting 'mercator' at the moment,
        raises `NotImplementedError` if other is passed
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.
    
    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys

    >>> print(zoom_center((-109.031387, -103.385460),
    ...     (25.587101, 31.784620)))
    (5.75, {'lon': -106.208423, 'lat': 28.685861})
    """
    if lons is None and lats is None:
        if isinstance(lonlats, tuple):
            lons, lats = zip(*lonlats)
        else:
            raise ValueError(
                'Must pass lons & lats or lonlats'
            )
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    if projection == 'mercator':
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            f'{projection} projection is not implemented'
        )
    
    return zoom, center


def getCoordinates(df_mapbox, ACCESS_TOKEN,
                      country = 'HU'):
    
    if country == 'DEU': country = 'DE'
    elif country == 'AUT': country = 'AT'
    elif country == 'SPA': country ='ES'

    pmeters = { 'limit': 1,
                'country': country,
                'types': 'region,postcode,district,place,locality,neighborhood,address',
                'autocomplete': 'false',
                'access_token': ACCESS_TOKEN
            }

    longitudes = []
    latitudes = []
    r_main = 0
    highest_relevance = 0
    for _ in range(len(df_mapbox['Location'])):
        if 'város' in df_mapbox["Location"][_]:
            query = str(re.split('\\W+', df_mapbox["Location"][0])[0]) #str(df_mapbox["Location"][_].split(',')[0])
        else:
            query = up.quote(str(df_mapbox["Location"][_]))
            print(query)
        URL = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json'
        r = requests.get(URL, params=pmeters)
        print(r.json())
        if r.json()['features']:
            if highest_relevance < 0.95:
                try:
                    query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[0]))
                except:
                    query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[1]))
                URL = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json'
                r = requests.get(URL, params=pmeters)
                if r.json()['features'] and r.json()['features'][0]['relevance'] > highest_relevance:
                    highest_relevance = r.json()['features'][0]['relevance']
                    r_main = r
            
            if r.json()['features'] and r.json()['features'][0]['relevance'] < 0.95:
                try:
                    query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[0]))
                except:
                    query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[1]))
                URL = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json'
                r = requests.get(URL, params=pmeters)
                if not r.json()['features']:
                    r = r_main
                else:
                    if r.json()['features'][0]['relevance'] < 0.95:
                        r = r_main

        if not r.json()['features']:
            try:
                query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[0]))
            except:
                query = up.quote(str(re.split('\\W+', df_mapbox["Location"][_].replace('/', ',').replace(' ,', ','))[1]))
            URL = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json'
            r = requests.get(URL, params=pmeters)
            if not r.json()['features']:
                r = r_main
            else:
                if r.json()['features'][0]['relevance'] < 0.95:
                    r = r_main
        try:
            longitudes.append(r.json()['features'][0]['geometry']['coordinates'][0])
            latitudes.append(r.json()['features'][0]['geometry']['coordinates'][1])
        except:
            longitudes.append(0)
            latitudes.append(0)
    return {'longitudes': longitudes, 'latitudes': latitudes}


def scatterChoropleth(df, ACCESS_TOKEN, country, coord = {}):
    df_mapbox = df.value_counts(['Location']).to_frame()
    df_mapbox.reset_index(inplace=True)
    print('coord: ', coord)
    if not coord:
        coord = getCoordinates(df_mapbox, ACCESS_TOKEN, country)
    df_mapbox['longitute'] = coord['longitudes']
    df_mapbox['latitude'] = coord['latitudes']
    zoom, center = zoom_center(lons = coord['longitudes'], lats = coord['latitudes'])
    fig = px.scatter_mapbox(df_mapbox,
                            lat = 'latitude',
                            lon = 'longitute',
                            mapbox_style='open-street-map',
                            # mapbox_style='carto-positron',
                            # width = 1200,
                            height = 600,
                            zoom = zoom - 1,
                            center = center,
                            size = 'count', size_max = 25)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    return fig, coord


def NopropertiesPrices(df, pr_mod, o1_mod, sale=0, r=0):
    if sale or r:
        x_t = f'Yearly Rental Price ({pr_mod[1:]})'
        x = df[f'Price_({pr_mod})'] * 12
        t = 'yearly rental prices'
    else:
        x_t = f'Price ({o1_mod})'
        x = f'Price_({pr_mod})'
        t = 'prices'
    fig = px.histogram(df[f'Price_({pr_mod})'], x=x,
                    nbins=20, histfunc='sum', text_auto="count",
                    # title=f'Number of properties based on their {t}',
                    height = 600)
    fig.update_layout(yaxis_title="No. of Properties", xaxis_title=x_t)
    fig.data[0].hovertemplate = x_t + '=' + '%{x}<br>No of Flats=%{y}<extra></extra>'
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    #fig.add_annotation(x=100, y= 3, text=f"Flat prices above<br>100 Mil HUF:<br>{df['Price_(M_HUF)'][df['Price_(M_HUF)'] > 100].count()} nos")
    #fig.show()
    return fig


def NopropertiesColor(df, pr_mod, o1_mod, sale, r):
        if sale or r:
            x_t = f'Monthly Rental Price ({pr_mod[1:]})'
            t = 'monthly rental prices'
        else:
            x_t = f'Price ({o1_mod})'
            t = 'prices'
        fig = px.histogram(df[f'Price_({pr_mod})'], x=f'Price_({pr_mod})', # fig = px.histogram(df[df[f'Price_({pr_mod})'] < 100], x=f'Price_({pr_mod})',
                        nbins=20, color=df['Rooms_(no.)']+df['Half_Rooms_(no.)'], # nbins=20, color=df[df[f'Price_({pr_mod})'] < 100]['Rooms_(no.)']+df[df[f'Price_({pr_mod})'] < 100]['Half_Rooms_(no.)'],
                        labels={'color': 'Rooms inc.<br>half rooms'},
                                # title=f'Number of properties based on their {t}\
                                #         <br>Color coded the number of rooms inculding half rooms',
                                        text_auto=True,
                                        height=600)
        fig.update_traces(showlegend=True)
        fig.update_layout(yaxis_title="No. of Properties", xaxis_title=x_t)
        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
        # fig.add_annotation(x=100, y= 3, text=f"Flat prices above<br>100 Mil HUF:<br>{df[f'Price_({pr_mod})'][df[f'Price_({pr_mod})'] > 100].count()} nos")
        # fig.show()
        return fig


def Nopropertiesm2prices(df, pr_mod, o1_mod, upr_mod, sale=0, r=0):
    if sale or r:
        x_t = f'Monthly Rental Price ({pr_mod[1:]})'
        t = 'monthly rental prices'
        x = f'Price_({pr_mod})'
    else:
        x_t = f'Price ({o1_mod})'
        t = 'prices'
        x = f'Unit_price_({upr_mod})'
    fig = px.histogram(df, x=x, nbins=20, text_auto=True, height=600)
                    #title='Number of properties based on their ' + t
    fig.update_layout(yaxis_title="No. of Properties", xaxis_title=x_t)
    fig.data[0].hovertemplate = x_t + '=' + '%{x}<br>No of Properties=%{y}<extra></extra>'
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    # fig.show()
    return fig


def NopropertiesArea(df, ar_mod):
    fig = px.histogram(df, x=f'Area_({ar_mod})',
                    nbins=20, text_auto=True,
                    # title='Number of properties based on their Area',
                    height = 600)
    fig.update_layout(yaxis_title="No. of Properties", xaxis_title=f'Area ({ar_mod})')
    fig.data[0].hovertemplate = f'Area_({ar_mod})=' + '%{x}<br>No of properties=%{y}<extra></extra>'
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    # fig.show()
    return fig


def UnitprArea(df, to_scrap, pr_mod, upr_mod, ar_mod, o1_mod, sale=0, r=0, t=0):
    # zeros_visible = {}
    # zeros_visible[f'Price_({pr_mod})'] = []
    # print(zeros_visible)
    # for _ in range(len(df[f'Price_({pr_mod})'])):
    #     if df[f'Price_({pr_mod})'][_] <= 0:
    #         zeros_visible[f'Price_({pr_mod})'].append(5000)
    #     else:
    #         zeros_visible[f'Price_({pr_mod})'].append(df[f'Price_({pr_mod})'][_])
    # fig = px.scatter(df, x=f'Area_({ar_mod})', y=f'Unit price ({upr_mod})', size=zeros_visible[f'Price_({pr_mod})'], color="Rooms_(no.)",
    if sale or r:

        if t:
            size=f'Land_Area_({ar_mod})'
            color='Rooms_(no.)'
            labels={'Rooms_(no.)': 'Rooms (no.)'}

        else:
            size='Rooms_(no.)'
            if to_scrap == 'ingatlancom':
                color=f'Balconies_({ar_mod})'
            else:
                color=''
            labels={f'Balconies_({ar_mod})': f'Balconies ({ar_mod})'}
            
        y=f'Price_({pr_mod})'
        title_mod=['', size.replace('_', ' '), '', pr_mod]

    else:
        y=f'Unit_price_({upr_mod})'
        size=f'Price_({pr_mod})'
        color='Rooms_(no.)'
        labels={'Rooms_(no.)': 'Rooms (no.)'}
        title_mod=['Unit ', f'Price ({o1_mod})', 'Unit ', upr_mod]
    if color:
        fig = px.scatter(df, x=f'Area_({ar_mod})', y=y, size=size, color=color,
                        log_x=False, size_max=20,
                        # title=f'{title_mod[0]}Price in the view of the Area' + '<br>' +  f'<span style="font-size: 12px;">Size: {title_mod[1]}</span>',
                        labels=labels, color_continuous_scale=px.colors.sequential.Blues_r, height = 600)
    else:
        fig = px.scatter(df, x=f'Area_({ar_mod})', y=y, size=size,
                        log_x=False, size_max=20,
                        # title=f'{title_mod[0]}Price in the view of the Area' + '<br>' +  f'<span style="font-size: 12px;">Size: {title_mod[1]}</span>',
                        labels=labels, height = 600)
    fig.update_layout(yaxis_title=f'{title_mod[2]}Price ({title_mod[3]})', xaxis_title=f'Area ({ar_mod})', showlegend=True)
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    # fig.show()
    return fig


def HeatHist(df, pr_mod, o1_mod, ar_mod, sale = 0, r = 0):
    if sale or r:
        y_t = f'Monthly Rental Price ({pr_mod[1:]})'
        t = 'Monthly Rental Prices'
    else:
        y_t = f'Price ({o1_mod})'
        t = 'Prices'


    fig = px.density_heatmap(df, x=f'Area_({ar_mod})', y=f'Price_({pr_mod})',
                            marginal_x="histogram",
                            marginal_y="histogram",
                            text_auto=True,
                            # title=t + ' of properties based on their Areas',
                            color_continuous_scale=px.colors.sequential.Blues_r,
                            height=600)
    fig.update_layout(yaxis_title=y_t, xaxis_title=f'Area ({ar_mod})')
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="White")
    return fig