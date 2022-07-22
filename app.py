# %%
import contextlib
import time
from unicodedata import name
import pandas as pd
import streamlit as st
import psycopg2
import sys
import numpy as np
from datetime import datetime, timedelta
import time
from PIL import Image
import requests
import json
from datetime import date

today = date.today()
today_formatted = today.strftime("%d.%m.%Y")
# %%
# Creating the Titles and Image
image = Image.open('dk-logo-black.png')
st.image(image) # , use_column_width=True)
st.title("DK - Cool MWA Tool")
st.write("Creating a cool Market analysis on the basis of Propstack data")
# %%
# api_key = st.text_input("Enter your API key") # get api from user

api_key = 'GIUi85PzLnOyegzs4idAXMhY5Jd_Fzj4gYy6P5T8'
url = "https://api.propstack.de/v1/"
# TODO add cache to query only once an hour
search = st.text_input("Search for an object, searches in unit_id, street, zip_code, city, Bezirk, exposee_id", 644102)
if len(search) != 0:
    object = f"units?q={search}"
    headers = {'X-API-KEY': '{key}'.format(key=api_key), 'per': '100'}
    response = requests.get(url+object, headers=headers)
    print(response.json())
    data_table = pd.DataFrame(response.json())
    try:
        short_data = data_table[['id','name','unit_id', 'street', 'zip_code', 'city', 'exposee_id']]
        st.write(short_data)
    except:
        short_data = pd.DataFrame()
        st.subheader("error, nothing to display")
# %%
    if 'id' in short_data.columns:
        objectid = str(st.selectbox('choose the object',short_data['id']))

# %%
        if len(objectid) != 0:
            object = f"documents?property={objectid}"
            headers = {'X-API-KEY': '{key}'.format(key=api_key)}
            response = requests.get(url+object, headers=headers)
            dict_response = json.loads(response.text)
            print(dict_response)
            number_of_files = dict_response['meta']['total_count']
            urls = [li['url'] for li in dict_response['documents']]
            st.write(urls)
            unit_link = f"units/{objectid}"
            response = requests.get(url+unit_link, headers=headers)
            dict_response = json.loads(response.text)
            st.json(dict_response)
# %% making input fields with default values from the website
            st.subheader("MWA Details")
            st.write("This is the MWA details of the selected object")
            date_input = st.text_input("Date of MWA", today_formatted)
            strasse_input = st.text_input("Street of Object", dict_response['street'])
# %%