import streamlit as st
from PIL import Image
import pandas as pd
import requests
import json
# pip install plotly==4.12.0
import plotly.express as px
import plotly.io as pio
import plotly.offline as pyo

apikey = st.secrets.apikey
url = "https://api.propstack.de/v1/"

image = Image.open('dk-logo-black.png')
st.image(image) # , use_column_width=True)
st.title("DK Takeover Map")
st.write("Where do we stand in overtaking Berlin?")
###############################################################################
object = f"property_statuses"
headers = {'X-API-KEY': '{key}'.format(key=apikey)}
response = requests.get(url+object, headers=headers)
data_table = pd.DataFrame(response.json()['data'])
st.write(data_table) #['total_count']
###############################################################################
# get the total number of units
"""
object = f"units?with_meta=1" # with_meta=1
response = requests.get(url+object, headers=headers).json()
total_objects = response['meta']['total_count']
per_page = 20
pages = (-(-total_objects//per_page)) # use floor division to round the page number up
#pages = 5
total_data = pd.DataFrame()
for page in range(pages):
    object = f"units?with_meta=1&page={page+1}" # with_meta=1
    response = requests.get(url+object, headers=headers).json()
    data_table = pd.DataFrame(response['data'])
    total_data = pd.concat([total_data, data_table])
# show the whole df
#st.write(total_data)  

def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(total_data)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)"""
###############################################################################
# object = f"units?page=3?with_meta=1" # with_meta=1
# headers = {'X-API-KEY': '{key}'.format(key=apikey)}
# response = requests.get(url+object, headers=headers).json()
# #st.write(response)
# st.write(response)
# data_table = pd.DataFrame(response)
# st.write(data_table)

def get_coordinates():
    df = pd.read_csv('data.csv')
    df.dropna(subset=['lat', 'lng'], inplace=True)
    lat = df['lat']
    lon = df['lng']
    df = df[['lat', 'lng']]
    df.columns = ['lat', 'lon']
    st.write(df.head())
    return df

# documentation on mapbox with plotly: https://plotly.com/python/mapbox-tutorial/
# https://plotly.com/python/mapbox-layers/
# https://plotly.com/python-api-reference/generated/plotly.express.scatter_mapbox.html

# df = get_coordinates()
# st.map(df, zoom=6) #default map
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
    # Warning-causing lines of code here
df = pd.read_csv('data.csv')
df.dropna(subset=['lat', 'lng'], inplace=True)
# convert status column to dict from string
from ast import literal_eval
df['status2'] = df.status.apply(lambda x: literal_eval(str(x)))
df_new = pd.concat([df, df['status2'].apply(pd.Series)], axis=1)
columns = ['unused', 'id', 'name', 'title', 'unit_id', 'exposee_id',
       'project_id', 'street', 'house_number', 'district', 'region',
       'zip_code', 'city', 'country', 'address', 'short_address', 'lat', 'lng',
       'number_of_rooms', 'price', 'base_rent', 'living_space',
       'number_of_bed_rooms', 'number_of_bath_rooms', 'property_space_value',
       'images', 'status', 'free_from', 'rented', 'status2', 'id_unused', 'status_name',
       'color']
df_new.columns = columns
# %%
#   df2.dropna(subset=['color'], inplace=True)
df_new.dropna(subset=['color', 'status_name'], inplace=True)
token = st.secrets.token
fig = px.scatter_mapbox(df_new, lat="lat", lon="lng", hover_name="name", hover_data=["street", "id"],
                        color=df_new["status_name"], zoom=10, center=dict(lat=52.52, lon=13.4), height=600)

fig.update_layout(mapbox_style="basic", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=False, sharing="streamlit")