import streamlit as st
from PIL import Image
import pandas as pd
import requests
import json

apikey = st.secrets.apikey
url = "https://api.propstack.de/v1/"

image = Image.open('dk-logo-black.png')
st.image(image) # , use_column_width=True)
st.title("DK Overtake Map")
st.write("Where do we stand in overtaking Berlin?")
###############################################################################
object = f"property_statuses"
headers = {'X-API-KEY': '{key}'.format(key=apikey)}
response = requests.get(url+object, headers=headers)
data_table = pd.DataFrame(response.json()['data'])
st.write(data_table) #['total_count']
###############################################################################
# get the total number of units
object = f"units?with_meta=1" # with_meta=1
response = requests.get(url+object, headers=headers).json()
total_objects = response['meta']['total_count']
per_page = 20
pages = int(total_objects/per_page)
#pages = 5
total_data = pd.DataFrame()
for page in range(pages):
    object = f"units?with_meta=1&page={page+1}" # with_meta=1
    response = requests.get(url+object, headers=headers).json()
    data_table = pd.DataFrame(response['data'])
    total_data = pd.concat([total_data, data_table])
# show the whole df
st.write(total_data)  
# download the whole df  
# btn = st.download_button(
#     label="Press to download the MWA",
#     data=total_data.to_csv(total_data, index=False),
#     file_name="data.csv",
#     mime="application/octet-stream"
# )
###############################################################################
# object = f"units?page=3?with_meta=1" # with_meta=1
# headers = {'X-API-KEY': '{key}'.format(key=apikey)}
# response = requests.get(url+object, headers=headers).json()
# #st.write(response)
# st.write(response)
# data_table = pd.DataFrame(response)
# st.write(data_table)
