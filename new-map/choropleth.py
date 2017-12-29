#import library
import folium.plugins
import pandas as pd
import geopandas as gpd
import numpy as np


#create map
m = folium.Map([29.22889, 45], zoom_start=5,tiles='cartodbpositron')

#import and clean data
countryData = pd.read_csv('GDP.csv')
conflictData=pd.read_csv('Armed_Conflict_Fatalities_1989_2016.csv')
fill=pd.read_csv('fill.csv')
fill=fill.drop('Year',1)
gdf = gpd.read_file('countries.json')


#compute opacity
w, h = 26, 16;
n_periods=26
opacity=[[0 for x in range(h)] for y in range(w)]
for x in range(26):
    for y in range(16):
        opacity[x][y]=(fill.iloc[x][y]-fill.iloc[x].min())/(fill.iloc[x].max()-fill.iloc[x].min())
opacity_T=np.transpose(opacity)

#compute date index
dt_index = pd.date_range('1991', periods = n_periods, freq='A').strftime('%Y')

#compute heat map based on GDP
styledata = { }
for country in gdf.index: 
    df = pd.DataFrame({'color': '#707737' ,
                       'opacity': opacity_T[country]},
                      index = dt_index)
    styledata[country] = df


styledict = {
    str(country): data.to_dict(orient='index') for
    country, data in styledata.items()
}
 

g = folium.plugins.TimeSliderChoropleth(gdf.to_json(),
                                        fill_color='YlGn',
                                        styledict = styledict
).add_to(m)


df = pd.read_excel('newdata.xlsx', sheet_name='Sheet1')    

for n in range(16):
    name = df['Row Labels'][n]
    x = df['Sum of best_est'][n]
    y = df['Latitude'][n]
    z = df['Longitude'][n]
    if x==0:
        r = 0
    elif x<=10:
        r = 1
    elif  x<=50:
        r = 3
    elif x<=100:
        r = 5
    elif x<=1000:
        r = 10
    elif x<=5000:
        r = 15
    elif x<=10000:
        r = 20
    else:
        r = 30
    folium.CircleMarker([y, z],
                    radius=r,
                    popup=name + ': ' + str(x),
                    color='#AC0700',
                   ).add_to(m)
try:
    m.save('map.html')
    print ('Done')
except:
    print ('Some error occurred')

