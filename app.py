import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdp
import plotly.express as px
from PIL import Image

#df = pd.read_csv('labeled.csv', dtype={'': str})
df_fullname = pd.read_csv('full_name.csv', dtype={'': str})
df_final = pd.read_csv('full_final.csv', dtype={'': str})

'''
# Youth in the City RESULTs
'''
st.write(f" child poverty is often defined as the rate of children under 15 years old living in households which are beneficiaries of social welfare. As of december 2020, the child poverty is about 15% on nation level. What is the child poverty in Berlin?")
col1, col2, col3 = st.columns(3)
col1.metric("Child poverty", "26.88%", "min: 0.66%, max:74.68%")
col2.metric("Dynamic of child poverty (2018 to 2020)", "-1.20%", "min: -23.69%, max:18.42%")
col3.metric("Gini-index", "0.38")

st.write(f"We collected more than 50 features from two Berlin Open-sources and on different levels and preprocessed these data into 542 planning areas. What features are correlataed with the Child poverty?")

image = Image.open('features_coor_dropwelf.png')

st.image(image, caption='Features Correlation to Child poverty')

def get_columnname(option, df):
    df_filtern = df[df.fullname == option]
    return df_filtern.column_name.values[0]
def get_shortname(option, df):
    df_filtern = df[df.fullname == option]
    return df_filtern.shortname.values[0]
def get_unit(option, df):
    df_filtern = df[df.fullname == option]
    return df_filtern.unit.values[0]
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

st.write(f" Here is {option} in each Planning areas")

@st.cache
def get_plotly_data():
    geojson_path = 'geodata_readytouse.geojson'
    with open(geojson_path) as geofile:
        j_file = json.load(geofile)
    return j_file

geojson_file = get_plotly_data()

color = get_columnname(str(option), df_fullname)
shortname = get_shortname(str(option), df_fullname)
unit =get_unit(str(option), df_fullname)

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
        hover_data={'PLR_ID':False,'child_pov':True, 'bezirk':True, color: True}
        )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_colorbar= {'title':f"{shortname} in {unit}"})
fig.show()
st.plotly_chart(fig)

st.write(f"This is the clustering results on the migration data")

df = df_final[['PLR_ID','cluster', 'mig_rate', 'child_pov','PLR_NAME','bezirk']]
df["cluster"] = df["cluster"].map({
 0: 'First cluster',
 1: 'Second cluster',
 2: 'Third cluster',
 3: 'Fourth cluster'})

fig = px.choropleth_mapbox(df, geojson=geojson_file, color="cluster",
                           locations="PLR_ID",
                           center={"lat": 52.52, "lon": 13.40},
                           #color= "category",
                           color_discrete_map={'First cat':'red','Sec cat':'Yellow','Third cat':'Green', 'Fourth cat': 'Blue'},
                           mapbox_style="carto-positron",
                           zoom=9,
                           title='<b>COVID-19 cases in Canadian provinces</b>',
                            labels={'cases' : 'Number of Cases',
                            'category' : 'Category'},
                            hover_name='PLR_NAME',
                            hover_data={'cluster' : True, 'PLR_ID' : False, 'mig_rate':True, 'child_pov':True, 'bezirk':True}
                            )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
df_clustervalue = pd.read_csv('cluster_values.csv').drop(columns=["Unnamed: 0"])
st.table(df_clustervalue)
