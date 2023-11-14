import os
import datetime
import pandas as pd
import pickle


def date_time():
    today = datetime.date.today()
    return today.strftime("%d, %B, %Y")

def modifiers(t,r,to_scrap):
    ch_price = ''
    ch_price_color = ''
    ch_unitpr = 'Unit '
    ch_scatter = ['Price', 'color: Rooms']
    df_heat = 'Area '
    prior_1 = 'Unit price'
    prior_2 = 'Area '

    if r:
        ch_price = 'Yearly Rental '
        ch_price_color = 'Monthly Rental '
        ch_scatter[0] = 'Rooms'
        prior_1 = 'Area'
        if t:
            df_heat = 'Land Area '
            ch_unitpr = 'Monthly Rental '
            ch_scatter[0] = 'Land Area'
            prior_2 = 'Land Area '
            if to_scrap == 'ingatlancom':
                ch_scatter[0] = 'Rooms'
                ch_scatter[1] = 'color: Balconies'
            else:
                ch_scatter[0] = 'Rooms'
                ch_scatter[1] = ''
                ch_unitpr = 'Unit '
        else:
            df_heat = 'Rooms '
            prior_2 = 'Rooms '

    if t:
        df_heat = 'Land Area'
        prior_2 = 'Land Area '

    return ch_price, ch_price_color, ch_unitpr, ch_scatter, df_heat, prior_1, prior_2

# #### Making dirs
def dir_creator():
    dirs = {'main_dir': 'files',
            'png_dir': 'files/png'}
    for _, v in dirs.items():
        if not os.path.exists(v):
            os.makedirs(v)
    return dirs

# #### Delete files
def delete_files(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)


def save_files(df, search_crit, to_scrap, filtered = ''):
    directory = 'files'
    # Save df in pickle file
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not df.empty:
        if search_crit:
            if filtered:
                filename = f"{(search_crit).replace(' ', '_')}_filtered"
            else:
                filename = f"{(search_crit).replace(' ', '_')}"
        else:
            if filtered:
                filename = f"{to_scrap}_webaddress_search_filtered"
            else:
                filename = f"{to_scrap}_webaddress_search"
        file_path = os.path.join(directory, filename)
        with open(file_path, "wb") as file:
            pickle.dump(df, file)
            df.to_csv(f"{file_path}.csv", index=False)

        return df, filename


def df_creator(to_scrap, result = [], t = 0, r = 0, sale = 0, pr_mod = 'CUR', upr_mod = 'CUR/m\u00b2', ar_mod = 'm\u00b2'):
    if to_scrap == 'ingatlancom':
        print(to_scrap, result, t, r, sale, pr_mod, upr_mod, ar_mod)
        if sale == 0:
            if t == 1:

                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[3][:-1],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Land_Area_({ar_mod})": result[0],
                        f"Price_({pr_mod})": result[4],
                        f"Unit_price_({upr_mod})": result[5],
                        "Location": result[6],
                        "Link": result[7],
                    }
                )
            else:

                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Balconies_({ar_mod})": result[3],
                        f"Price_({pr_mod})": result[4],
                        f"Unit_price_({upr_mod})": result[5],
                        "Location": result[6],
                        "Link": result[7],
                    }
                )
        elif sale == 1:
            if t == 1:

                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[3][:-1],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Land_Area_({ar_mod})": result[0],
                        f"Price_({pr_mod})": result[4],
                        "Location": result[6],
                        "Link": result[7],
                    }
                )
            else:

                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Balconies_({ar_mod})": result[3],
                        f"Price_({pr_mod})": result[4],
                        "Location": result[6],
                        "Link": result[7],
                    }
                )
    elif to_scrap == 'immoscout24':
        if r == 0:
            unit_price = []
            for _ in range(len(result[3])):
                try:
                    unit_price.append(result[3][_] / result[0][_])
                except:
                    unit_price.append(0)
            if t == 1:
                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Land_Area_({ar_mod})": result[6],
                        f"Price_({pr_mod})": result[3],
                        f"Unit_price_({upr_mod})": unit_price,
                        "Location": result[4],
                        "Link": result[5],
                    }
                )
            else:
                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Price_({pr_mod})": result[3],
                        f"Unit_price_({upr_mod})": unit_price,
                        "Location": result[4],
                        "Link": result[5],
                    }
                )
                print(df)
        elif r == 1:
            if t == 1:

                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Land_Area_({ar_mod})": result[6],
                        f"Price_({pr_mod})": result[3],
                        "Location": result[4],
                        "Link": result[5],
                    }
                )
            else:
                df = pd.DataFrame(
                    {
                        f"Area_({ar_mod})": result[0],
                        "Rooms_(no.)": result[1],
                        "Half_Rooms_(no.)": result[2],
                        f"Price_({pr_mod})": result[3],
                        "Location": result[4],
                        "Link": result[5],
                    }
                )

    return df

def titles_text(ch_price, ch_price_color, ch_unitpr, ch_scatter, prior_1, prior_2, data_source = '', country_source = '', date_time = date_time()):
    return {
'cover_title': [
'Real Estate Data Insights Report',
'Exploring Prices, Areas, and Property Details',
f'Data source: {data_source}, Country: {country_source}, Date: {date_time}',
'black'
],
'intro': [
'Introduction',
'Unraveling Insights from Our Data',
"Within the pages of this report lies a treasure trove of insights and revelations drawn from our meticulously collected data. As we embark on this journey, you'll find a rich tapestry of information brought to life through a series of tables and charts.\n\n\
Our dataset is a fascinating landscape of details and trends, waiting to be explored. The tables reveal intricate statistics, key figures, and vital metrics that form the backbone of our analysis. From property distributions to pricing patterns, these tables provide the numerical foundation upon which we build our understanding.\n\n\
But that's not all. The charts, a visual tour de force, transform raw data into compelling narratives. They highlight property distributions based on area and price, unveil the relationship between pricing and room configurations, and showcase concentration areas of properties. In scatter plots and choropleths, you'll witness the dynamic interplay of data points, offering nuanced insights into our dataset.\n\n\
Our mission is to transform data into knowledge. As you peruse these tables and charts, you'll uncover the narratives that lie within the numbers and patterns. This is not just data; it's the key to informed decision-making, and it all begins here. Welcome to the world of insights, where tables and charts are our guiding lights.", 'black'],
'chapter_1': '1. Tables',
'df_describe': [
'Dataframe key details', '',
"This is a short summary of the data. Here you can find general details of all the columns in the dataframe.\n\
Count shows the total number of rows.\nMean is the column's mean value.\n\
Std is the standard deviation of the columns data.\n\
Min is the minimum, max is the maximum value.\n\
The percentages indicate the maximum values of the indicated percentage of all values.", 'black'],
'df_maxes': [
'Maximum values of all the columns', '',
'Highlighted all the maximum values of the actual columns. \
In case of more cells highlighted in a row \
means the particular property has maximum value in more than one property.', 'black'],
'df_mins': [
'Minimum values of all the columns', '',
'Highlighted all the minimum values of the actual columns. \
In case of more cells highlighted in a row \
means the particular property has minimum value in more than one property.', 'black'],
'df_heat_maxes': [
f'Sorted data by Price > {prior_1} > {prior_2}in descending order', '',
f'The sorting criteria Price first, \
{prior_1} second, {prior_2}third. Includes the first 15 rows.', 'black'],
'df_heat_mins': [
f'Sorted data by Price > {prior_1} > {prior_2}in descending order', '',
f'The sorting criteria Price first, \
{prior_1} second, {prior_2}third. Includes the first 15 rows.', 'black'],
'df_mid': [
'Middle value / values (closest to the mean of Area)', '',
"Colored bars indicate how high the actual cell value is. \
Maximum bar length is equal to the cell length, \
minimum bar length is 'zero' (no bar). The color deepens as the value increases.", 'black'],
'chapter_2': '2. Charts',
'ch_area': [
'Number of properties based on their Areas', '',
'This histogram shows the number of properties by areas with bin size of 20. \
Area is usually the net usable surface where carpet can be laid (i.e RARE in the US), \
which excludes areas covered by external walls, areas under service shafts, \
exclusive balcony or verandah area and exclusive open terrace. The net usable area also depends on the height of the premise \
e.g under roofs intersecting the clear height of the room', 'black'],
'ch_price': [
f'Number of properties based on their {ch_price}Prices', '',
f'This histogram shows the {ch_price}price range of the properties using a bin size of 20.\n \
A few main factors to influence real estate prices are:\n\
the location - how accessible the schools, shops, how are the employment opportunities, \
size - usable space, age and condition - typically, homes that are newer appraise at a higher value, \
upgrades and updates - kitchen remodel, pool etc. can add value to the property, \
the local market - is it a buyer or a seller market, \
economic indicators - how easily can people afford homes, \
interest rate - influence the ability people can buy homes.', 'black'],
'ch_price_color': [
f'Number of properties based on their {ch_price_color}Prices', 'Color coded the number of rooms including half rooms',
f'This histogram shows the {ch_price_color} price range of the properties using a bin size of 20.\
Room nos. include bedroom, living room, study, office, family room, and other type of rooms \
but does not include kitchen, dining room, bathroom.\n\
The definition of half room depends on the country and applicable regulations. \
In Germany the half room is a room below 10 m\u00b2, in Hungary the same is considered below 12 m\u00b2.', 'black'],
'ch_unitpr': [
f'Number of properties based on their {ch_unitpr}Prices', '',
f'This histogram shows the {ch_unitpr}price range of the properties using a bin size of 20.\
The median monthly rental prices in the most expensive region of the capital/most important city for a 1-bedroom apartment in the EU as of 2023 September:\n\
Italy, Milan - 2875 EUR, Switzerland, Zurich - 2623 EUR, France, Paris - 1900 EUR, Spain, Madrid - 1500 EUR, Austria, Vienna - 1090 EUR, \
Germany, Berlin - 760 EUR, Hungary, Budapest - 675 EUR.', 'black'],
'ch_heathist': [
f'{ch_price_color}Prices of properties based on their Areas', '',
f'Heat map and histograms showing the {ch_price_color}Price. Histograms show the count of the Area and Price.', 'black'],
'ch_scatter': [
f'{ch_unitpr}Price in the view of the Area', f'size: {ch_scatter[0]}, {ch_scatter[1]}',
f'This chart shows the relation of the {ch_unitpr}Price and the Area.\n\
On this diagram you can see the correlation between the indicated factors represented by the size and colors (if applicable). \
The Unit Price and the Area are typically negatively correlated while the Room nos. and the Area are positively correlated.', 'black'],
'ch_choropleth': [
'Choropleth showing the Locations', 'size: Quantity',
'To have a better understanding of the location the choropleth represents the properties on the map, the size indicates the numbers of the properties on those areas.\n\
In those cases when the exact address is not provided the location of the center of the searched area (city) indicated', 'gainsboro']
}