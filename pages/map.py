import streamlit as st
st.set_page_config(layout="wide") # wide, boxed, centered
from PIL import Image
import pandas as pd
import requests
import json
# pip install plotly==4.12.0
import plotly.express as px

@st.cache(ttl=60*60*24, allow_output_mutation=True) # cache for 1 day
def get_data():
    object = f"units?with_meta=1" # with_meta=1
    headers = {'X-API-KEY': '{key}'.format(key=apikey)}
    response = requests.get(url+object, headers=headers).json()
    total_objects = response['meta']['total_count']
    per_page = 20
    pages = (-(-total_objects//per_page)) # use floor division to round the page number
    total_data = pd.DataFrame()
    for page in range(pages):
        object = f"units?with_meta=1&page={page+1}" # with_meta=1
        response = requests.get(url+object, headers=headers).json()
        data_table = pd.DataFrame(response['data'])
        total_data = pd.concat([total_data, data_table])
    return total_data

def convert_df(df):
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    from ast import literal_eval
    df['status2'] = df.status.apply(lambda x: literal_eval(str(x)))
    df_new = pd.concat([df, df['status2'].apply(pd.Series)], axis=1)
    columns = ['id', 'name', 'title', 'unit_id', 'exposee_id',
       'project_id', 'street', 'house_number', 'district', 'region',
       'zip_code', 'city', 'country', 'address', 'short_address', 'lat', 'lng',
       'number_of_rooms', 'price', 'base_rent', 'living_space',
       'number_of_bed_rooms', 'number_of_bath_rooms', 'property_space_value',
       'images', 'status', 'free_from', 'rented', 'status2', 'id_unused', 'status_name',
       'color']
    df_new.columns = columns
    df_new.dropna(subset=['color', 'status_name'], inplace=True)
    return df_new

def make_map(df_new):
    fig = px.scatter_mapbox(df_new, lat="lat", lon="lng", hover_name="name", hover_data=["street", "id"],
                        color=df_new["status_name"], zoom=10, center=dict(lat=52.52, lon=13.4), height=600)
    fig.update_layout(mapbox_style="basic", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

apikey = st.secrets.apikey
token = st.secrets.token
url = "https://api.propstack.de/v1/"

image = Image.open('dk-logo-black.png')
st.image(image) # , use_column_width=True)
st.title("DK Takeover Map")
st.write("Where do we stand in overtaking Berlin?")

# get data
df = convert_df(get_data())
# make a map
st.plotly_chart(make_map(df), use_container_width=True, sharing="streamlit")