import pandas as pd
import numpy as np
# import dataframe_image as dfi


def df_filter(df, pr_mod, upr_mod, ar_mod): 
        min_modifier = 0.9
        max_modifier = 4
        mean_area = df[f'Area_({ar_mod})'].mean()
        mean_rooms = df['Rooms_(no.)'].mean()
        mean_price = df[f'Price_({pr_mod})'].mean()

        filter_condition = (
                (df[f'Area_({ar_mod})'] >= mean_area - mean_area*min_modifier) &
                (df[f'Area_({ar_mod})'] <= mean_area + max_modifier * mean_area) &
                (df['Rooms_(no.)'] >= mean_rooms - mean_rooms*min_modifier) &
                (df['Rooms_(no.)'] <= mean_rooms + max_modifier * mean_rooms) &
                (df[f'Price_({pr_mod})'] >= mean_price - mean_price*min_modifier) &
                (df[f'Price_({pr_mod})'] <= mean_price + max_modifier * mean_price))

        if f'Unit_price_({upr_mod})' in df.columns:
                mean_unit_price = df[f'Unit_price_({upr_mod})'].mean()
                filter_condition = filter_condition & (
                (df[f'Unit_price_({upr_mod})'] >= mean_unit_price - mean_unit_price*min_modifier) &
                (df[f'Unit_price_({upr_mod})'] <= mean_unit_price + max_modifier * mean_unit_price))
        if f'Land_Area_({ar_mod})' in df.columns:
                mean_land_area = df[f'Land_Area_({ar_mod})'].mean()
                filter_condition = filter_condition & (
                (df[f'Land_Area_({ar_mod})'] >= mean_land_area - mean_land_area*min_modifier) &
                (df[f'Land_Area_({ar_mod})'] <= mean_land_area + max_modifier * mean_land_area))

        return df[filter_condition]


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{"link"}</a>'


def df_describe_styled(df):
    return df.describe()\
    .rename(columns=lambda x: x.replace('_', ' '))\
    .style.format(precision=0, thousands=" ", decimal=".")


def df_maxes_styled(df):
    max_indices = df.idxmax()
    df_maxes = pd.DataFrame(columns = df.columns)
    for i in range(len(max_indices)-2):
        if i >= 1 and max_indices.iloc[i] == max_indices.iloc[i-1]:
            continue
        else:
            new_row = pd.DataFrame(df.loc[max_indices.iloc[i]]).T
            if new_row.index[0] in df_maxes.index:
                continue
            df_maxes = pd.concat([df_maxes, new_row])
    df_maxes = df_maxes.rename(columns=lambda x: x.replace('_', ' '))
    return df_maxes.style.format({'Link': make_clickable}, precision=0, thousands=" ", decimal=".")\
        .highlight_max(subset = df_maxes.columns[:-2], color='lightgreen')


def df_mins_styled(df):
    min_indices = df.idxmin()
    df_mins = pd.DataFrame(columns = df.columns)
    for i in range(len(min_indices)-2):
        if i >= 1 and min_indices.iloc[i] == min_indices.iloc[i-1]:
            continue
        else:
            new_row = pd.DataFrame(df.loc[min_indices.iloc[i]]).T
            if new_row.index[0] in df_mins.index:
                continue
            df_mins = pd.concat([df_mins, new_row])
    df_mins = df_mins.rename(columns=lambda x: x.replace('_', ' '))
    return df_mins.style.format({'Link': make_clickable}, precision=0, thousands=" ", decimal=".")\
        .highlight_min(subset = df_mins.columns[:-2], color='lightcoral')


def df_heat_maxes_styled(df, pr_mod, ar_mod, upr_mod, r, t):
    prior_1 = f'Unit price ({upr_mod})'
    prior_2 = f'Area ({ar_mod})'
    if r:
        prior_1 = f'Area ({ar_mod})'
        if t:
            prior_2 = f'Land Area ({ar_mod})'
        else:
            prior_2 = 'Rooms (no.)'
    if t:
        prior_2 = f'Land Area ({ar_mod})'
    return df.rename(columns=lambda x: x.replace('_', ' ')).sort_values(by=[f'Price ({pr_mod})', prior_1, prior_2], ascending=False)\
            .head(15)\
            .style\
            .format({'Link': make_clickable}, precision=0, thousands=" ", decimal=".")\
            .background_gradient(axis=0)



def df_heat_mins_styled(df, pr_mod, ar_mod, upr_mod, r, t):
    prior_1 = f'Unit price ({upr_mod})'
    prior_2 = f'Area ({ar_mod})'
    if r:
        prior_1 = f'Area ({ar_mod})'
        if t:
            prior_2 = f'Land Area ({ar_mod})'
        else:
            prior_2 = 'Rooms (no.)'
    if t:
        prior_2 = f'Land Area ({ar_mod})'
    return df.rename(columns=lambda x: x.replace('_', ' ')).sort_values(by=[f'Price ({pr_mod})', prior_1, prior_2], ascending=True)\
            .head(15)\
            .style\
            .format({'Link': make_clickable}, precision=0, thousands=" ", decimal=".")\
            .background_gradient(axis=0)


def df_mid_styled(df, ar_mod):
    np.seterr(divide='ignore', invalid='ignore')
    areas = list(df[f'Area_({ar_mod})'])
    avg_areas = df[f'Area_({ar_mod})'].mean()
    mid_element = df.loc[df[f'Area_({ar_mod})'] == avg_areas - min([abs(elem - avg_areas) for elem in areas])]
    if mid_element.empty:
        mid_element = df.loc[df[f'Area_({ar_mod})'] == avg_areas + min([abs(elem - avg_areas) for elem in areas])]

    bigger_10 = df.sort_values(by=f'Area_({ar_mod})')\
        .loc[df.sort_values(by=f'Area_({ar_mod})')[f'Area_({ar_mod})'] >
            float(mid_element[f'Area_({ar_mod})'].iloc[0])].head(8)
    smaller_10 = df.sort_values(by=f'Area_({ar_mod})', ascending=False)\
        .loc[df.sort_values(by=f'Area_({ar_mod})', ascending=False)[f'Area_({ar_mod})'] < 
            float(mid_element[f'Area_({ar_mod})'].iloc[0])].head(8)\
                .sort_values(by=f'Area_({ar_mod})', ascending=True)
    df_mid = pd.concat([smaller_10, mid_element, bigger_10], axis=0)
    length_df = df_mid.shape[0]
    if length_df > 18:
        rows_tocut = int((length_df - 17)/2)
        if rows_tocut != 0:
            df_mid = df_mid[rows_tocut:-rows_tocut]
    return df_mid\
        .rename(columns=lambda x: x.replace('_', ' '))\
        .style.format({'Link': make_clickable}, precision=0, thousands=" ", decimal=".")\
        .bar(align='left', cmap='Blues', height=60, width=95, props="width: 0px;")\
        .text_gradient(cmap='gist_gray')#.hide(axis=0)
        #.iloc[:,:-1]\