import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px

df = pd.read_csv('labeled.csv', dtype={'': str})
df_fullname = pd.read_csv('full_name.csv', dtype={'': str})
df_final = pd.read_csv('fullcleaned.csv', dtype={'': str})

'''
# Youth in the City RESULTs
'''
st.write(f"Try to show the ugly facts about child poverty in Berlin")
col1, col2, col3 = st.columns(3)
col1.metric("Child poverty", "24.54%", "min: 0.66%, max:74.68%")
col2.metric("Dynamic of child poverty (2018 to 2020)", "-1.04%", "min: -23.69%, max:18.42%")
col3.metric("Gini-index", "0.38")

def get_columnname(option, df):
    df_filtern = df[df.fullname == option]
    return df_filtern.column_name.values[0]
def get_fullname(column_name, df):
    df_filtern = df[df.column_name == column_name]
    return df_filtern.fullname.values

option = st.selectbox('Which feature do you like to see on Berlin Maps?',
     ('Population with migration background in %',
 'Unemployment in %',
 'Welfare beneficiaries in %',
 'Child poverty in %',
 'Dynamic of unemployment in % (2018 to 2020)',
 'Dynamic of welfare in % (2018 to 2020)',
 'Dynamic of child poverty in % (2018 to 2020)',
 'Average advertised rent in €/m2',
 'Social housing in %',
 'Share of municipal housing companies in the housing stock in %',
 'Conversion of multi-family houses into condos in %',
 'Dynamic of condo conversion in % (2015 to 2020)',
 'Aparments sale in %',
 'Dynamic of apartment sales in % (2015 to 2020)',
 'Share of inhabitants with at least 5 years of residence in %',
 'Amount of public transport stops within 500 m, incl. bus',
 'Amount of restaurants and cafés within 500 m (exc. fast food)',
 'Amount of cultural institutions within 500 m (museums, cinemas, theaters, etc.)',
 "Amount of extra-curriculum educational institutions within 500 m (music and language schools)'",
 'Amount of urban furniture (picnic tables, benches, bbq, water points, etc.) within 500 m',
 'Amount of places for outdoor leisure (swimming pools, parks, playgrounds, etc.) within 500 m',
 'Amount of bars, pubs, nightclubs, etc. within 500 m',
 'Share of houses built before 1940 in % (as of 2015)',
 'Share of houses built between 1941 and 1991 in % (as of 2015)',
 'Share of houses built between 1991 and 2001 in % (as of 2015)',
 'Vegetation volume in m3/m2',
 'Amount of other types of schools',
 'Amount of vocational schools',
 'Amount of primary schools',
 'Amount of Gymnasiums',
 'Amount of other secondary schools',
 'Amount of private schools',
 'Amount of schools for children with special needs',
 'Amount of kindergartens',
 'Amount of rail / U-bahn / S-bahn and tram stations'))

st.write(f" Here is {option} in each Planningarea")

@st.cache
def get_plotly_data():
    geojson_path = 'geodata_readytouse.geojson'
    df = pd.read_csv('labeled.csv', dtype={'': str})
    with open(geojson_path) as geofile:
        j_file = json.load(geofile)
    return df, j_file

df, geojson_file = get_plotly_data()

color = get_columnname(str(option), df_fullname)
fig = px.choropleth_mapbox(
        data_frame = df_final,
        geojson=geojson_file,
        locations="PLR_ID",
        color=color,
        color_continuous_scale="Viridis",
        range_color=(df_final[color].max(), df_final[color].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        opacity=0.5,
        #labels= {f"{color}: {color} amount"},
        hover_name='PLR_NAME',
        hover_data={'PLR_ID':False,'child_pov':True, 'BZR_NAME':True, color: True}
        )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_colorbar= {'title':""})
fig.show()

st.plotly_chart(fig)

#hover_data = {'a':True,'b':True, 'c':True, 'id':False}
multi_option = st.multiselect(
     'Which feature do you like to see by hovering your mouse?',
     ('public_tra', 'eating', 'culture', 'community', 'health_car',
       'public_ser', 'education', 'schools', 'universiti', 'kindergart',
       'outdoor_fa', 'outdoor_le', 'night_life', 'water', 'ave_rent',
       'social_hou', 'public_hou', 'dyn_ew', 'five_y_pls', 'dyn_sales',
       'child_pov', 'dyn_unempl', 'noise', 'air', 'green', 'bio', 'B_age',
       'mig_rate', 'label', 'PLR_NAME', 'BZR_NAME'))
st.write(f" Here is the clustering result")


hover_datas = multi_option

fig = px.choropleth_mapbox(
        data_frame = df,
        geojson= geojson_file,
        locations="PLR_ID",
        color="label",
        #color_continuous_scale="Rainbow",
        #range_color=(df[color_option].max(), df[color_option].min()),
        mapbox_style="open-street-map",
        zoom=9,
        center={
            "lat": 52.52,
            "lon": 13.40
        },
        #labels= {f"{color_option}: {color_option} amount"},
        hover_name='PLR_NAME',
        hover_data= ['child_pov'] + hover_datas)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(
    title="clustering",
    thicknessmode="pixels",
    lenmode="pixels",
    yanchor="top",y=1,
    ticks="outside",
    tickvals=[0,1,2,3,4],
    ticktext=["0", "1", "2", "3"],
    dtick=4
))

st.plotly_chart(fig)
