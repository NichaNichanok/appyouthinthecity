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

st.header('Child poverty in Berlin')
st.write("")
st.write("")

st.markdown("More than one out of four children lives under poverty in Berlin. This is about 12 percent above the overall child poverty rate in Germany (15%).")

st.write("")

col1, col2, col3 = st.columns(3)
col1.metric("Berlin", "26.88%", "-1.20%")
col2.metric("Pankow", "0.66%", "0.02%")
col3.metric("Neukölln", "74.68%", "-1.63%")

st.write("")

st.write("Poverty is not only a material matter; it affects children’s everyday life, their social network, their educational chances, even their health. Associated with social segregation, which prevents children to be in touch with other milieus, it can become a hardly escapable trap.")

st.write("We collected more than 100 geodata features from [OpenStreetMaps](https://www.openstreetmap.org/#map=5/51.330/10.453) and [Berlin Open Data platform](https://daten.berlin.de/) and aggregated them to the level of the 542 planning areas, the smallest statistical areas, on which social data is publicly available.")

st.write("Which social or infrastructural features does child poverty correlate most with? This Wordclound displays a selection of the features we collected, which are sized according to their correlation (Pearson) with child poverty (See Fig.1).")

st.write("")
#st.write("")

image = Image.open('wc2.png')

st.image(image, caption='Fig.1: Features Correlation to Child poverty, data from Berlin Open Data platform shown in violet, OpenStreetMaps in orange, respectively')

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

#st.subheader("Here, you can plot a selection of features we processed and collected.", anchor=None)

option = st.selectbox('Here, you can plot a selection of features we processed and collected.',
     ('Child poverty in % per planning area',
 'Unemployment in % per planning area',
 'Welfare beneficiaries in % per planning area',
 'Population with migration background in % per planning area',
 'Dynamic of unemployment in % (2018 to 2020) per planning area',
 'Dynamic of welfare in % (2018 to 2020) per planning area',
 'Dynamic of child poverty in % (2018 to 2020) per planning area',
 'Average advertised rent in €/m2 per planning area',
 'Social housing in % per planning area',
 'Share of municipal housing companies in the housing stock in % per planning area',
 'Conversion of multi-family houses into condos in % per planning area',
 'Dynamic of condo conversion in % (2015 to 2020) per planning area',
 'Aparments sale in % per planning area',
 'Dynamic of apartment sales in % (2015 to 2020) per planning area',
 'Share of inhabitants with at least 5 years of residence in % per planning area',
 'Amount of public transport stops within 500 m, incl. bus per planning area',
 'Amount of restaurants and cafés within 500 m (exc. fast food) per planning area',
 'Amount of cultural institutions within 500 m (museums, cinemas, theaters, etc.) per planning area',
 "Amount of extra-curriculum educational institutions within 500 m (music and language schools) per planning area",
 'Amount of urban furniture (picnic tables, benches, bbq, water points, etc.) within 500 m per planning area',
 'Amount of places for outdoor leisure (swimming pools, parks, playgrounds, etc.) within 500 m per planning area',
 'Amount of bars, pubs, nightclubs, etc. within 500 m per planning area',
 'Share of houses built before 1940 in % (as of 2015) per planning area',
 'Share of houses built between 1941 and 1991 in % (as of 2015) per planning area',
 'Share of houses built between 1991 and 2001 in % (as of 2015) per planning area',
 'Vegetation volume in m3/m2 per planning area',
 'Amount of other types of schools per planning area',
 'Amount of vocational schools per planning area',
 'Amount of primary schools per planning area',
 'Amount of Gymnasiums per planning area',
 'Amount of other secondary schools per planning area',
 'Amount of private schools per planning area',
 'Amount of schools for children with special needs per planning area',
 'Amount of kindergartens per planning area',
 'Amount of rail / U-bahn / S-bahn and tram stations per planning area',
 'Population with EU15-origin in % per planning area', 'Population with EU28-origin in % per planning area',
 'Population with Poland-origin in % per planning area', 'Population with Ex-Yugoslavia-origin in % per planning area',
 'Population with Post-Soviet states-origin in % per planning area', 'Population with Turkey origin in % per planning area',
 'Population with Arab-origin in % per planning area', 'Population with Other-origin in % per planning area',
 'Population with not identified origin in % per planning area'))

#st.write(f" {option} per Planning areas")
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
        hover_data={'PLR_ID':False,'child_pov':True, 'Bezirk':True, color: True}
        )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_colorbar= {'title':f"{shortname} in {unit}"})
fig.show()
st.plotly_chart(fig)
st.write("")

st.write(f"Next, we used clustering to observe patterns in our data. Here is an example. We built 4 clusters on the mean social index (unemployment, welfare benefit and child poverty) and the share of persons with a migration background (See Fig.2).")
st.write("")
fig = px.choropleth_mapbox(df_final, geojson=geojson_file, color="Clusters",
                           locations="PLR_ID",
                           center={"lat": 52.52, "lon": 13.40},
                           color_discrete_map={'High social index, low migration rate':'orchid',
                                               'somewhat low social index, average migration rate':'violet',
                                               'average social index, average migration rate':'turquoise',
                                               'very low social index, very high migration rate': 'gold'},
                           mapbox_style="open-street-map",
                           zoom=9,
                           hover_name='PLR_NAME',
                           hover_data={'Cluster' : False, 'PLR_ID' : False, 'unemployme':True, 'welfare':True,
                                       'mig_rate':True, 'child_pov':True, 'Bezirk':True}
                            )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
st.plotly_chart(fig)
#st.write("The table below the map displays the standardized mean values of those variables for each cluster.")
image_clus = Image.open('cluster_cap.png')

st.image(image_clus, caption= "Fig.2: This table displays the standardized mean values of those variables for each cluster.")

st.write("")

st.write("Observing that child poverty correlates most with social data - it is actually constructed by it - we decided to try and identify patterns in its infrastructural context.")
st.write("Do child poverty hotspots lack infrastructures? What context, which infrastructural features influence the concentration of child poverty most in Berlin?")

st.write("We implemented several regression models on 10 infrastructural features (See Fig.3). With an R2 of 0.49, our best performing model (spatial lag regression differentiating between east and west Berlin), explains almost half of the variability of child poverty in Berlin with infrastructures!")
image_conc = Image.open('z_stat.png')

st.image(image_conc, caption="Fig.3: Feature's significance of 10 infrastructural features, calculated by spatial lag regression differentiating between east and west Berlin")

st.write("")
st.subheader("Findings")
st.write("")
st.write("Not surprisingly, we confirmed that the social context of child poverty is what influences its concentration most. The share of welfare beneficiaries, of persons with a migration background and of unemployed people are the strongest predictors for child poverty in Berlin’s planning areas.")
st.write("Against the idea of infrastructural deserts, which are observed in other cities, e.g. in the US, we found that child poverty is not systematically correlated with a lack of cultural institutions, outdoor facilities or schools. Berlin is a “well connected city” (Blokland, Vief. 2020).*")
st.write("")
st.markdown("Our model identified **two very significant features** for child poverty: **social housing and public housing**. Households with limited resources gather in places where there is a higher share of affordable rents. A uniform distribution of social and public housing throughout the city thus appears like the most direct way to fight against social segregation and child poverty hotspots in Berlin.")
st.write("The conclusion? Affordable housing is critical for the fight against social inequalities and the distribution of the housing stock can have very concrete consequences on children's individual lives and on society as a whole.")
st.write("")
_, colm, _ = st.columns([1, 2, 1])
with colm:
    st.subheader("Berlin fight poverty, stay sexy!")

st.write("")
st.write("This project was conducted by Maciej Szuba , Nichanok Auevechanichkul and Safia Ahmedou as part of a Data Science Bootcamp at Le Wagon (batch #874)  in September 2022.")
st.caption("*Note that the positive correlation of Kindergartens with child poverty in Eastern parts of the city might be biased; as we did not have data on their capacity, we only took their number in consideration.")
st.subheader("Sources:")
st.write("Andrew Deener, The Origins of the Food Desert: Urban Inequality as Infrastructural Exclusion, Social Forces, Volume 95, Issue 3, March 2017, Pages 1285–1309, https://doi.org/10.1093/sf/sox001")
st.write("Blokland, T., Vief, R. (2021). Making Sense of Segregation in a Well-Connected City: The Case of Berlin. In: van Ham, M., Tammaru, T., Ubarevičienė, R., Janssen, H. (eds) Urban Socio-Economic Segregation and Income Inequality. The Urban Book Series. Springer, Cham. https://doi.org/10.1007/978-3-030-64569-4_13")
st.write("Voss, P.R., Long, D.D., Hammer, R.B. et al. County child poverty rates in the US: a spatial regression approach. Popul Res Policy Rev 25, 369–391 (2006). https://doi.org/10.1007/s11113-006-9007-4")
st.write("SBJF. Berlin aktiv gegen Kinderarmut : Bericht der Landeskommission zur Prävention von Kinder- und Familienarmut / Herausgeber Senatsverwaltung für Bildung, Jugend und Familie. 2021. URN: https://nbn-resolving.de/urn:nbn:de:kobv:109-1-15448517")
st.write("")
st.write("")
st.caption("DISCLAIMER: We collected a part of our data from OpenStreetMap thanks to Overpass API. OpenStreetMap is a very precious open source project. The data on places (restaurants, cultural institutions, outdoor facilities, etc.) highly depends on volunteer contributions and might not be complete. ")
