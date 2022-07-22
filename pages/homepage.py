import collections
from numpy.core.defchararray import lower
import streamlit as st
import numpy as np
import pandas as pd


def app():
    st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis.") 
    st.write("\n")

    # Code to read a single file 
    file_excel = st.file_uploader("Upload Excel",type=['xlsx'])
    global data
    if file_excel is not None:
        data = pd.read_excel(file_excel, sheet_name='script', header=None, names=['keys', 'values'], na_values='(None)', usecols = 'A:B')
        print("Data uploaded successfully")
        data = data.fillna('')
        keys = data['keys'].tolist()
        values = data['values'].tolist()
        dictionary = dict(zip(keys, values))
        vorteile = ["Vorteil1","Vorteil2","Vorteil3","Vorteil4","Vorteil5","Nachteil1","Nachteil2",
        "Nachteil3","Nachteil4","Nachteil5", 'Resume1', 'Resume2', 'Resume3']
        # try bullet points
        # bullet_point = u'\u2022'
        for vorteil in vorteile:
            dictionary[vorteil]=str(dictionary[vorteil]).replace("0", "")
            # add bullet points in front
            # if dictionary[vorteil] != "":
            #     dictionary[vorteil]=bullet_point + " " + str(dictionary[vorteil])
        # print(dictionary)
        # makler provision text
        text = """Neues Gesetz zur Maklerprovision:""" 
        text1 = """Seit dem 23. Dezember 2020 gilt das neue Gesetz von CDU/CSU und SPD zur Maklerprovision. Dies sieht vor, dass sich Käufer und Verkäufer einer Immobilie bundesweit einheitlich die Courtage hälftig teilen. Mit dieser Regelung sind beide Parteien somit gleichermaßen an den Kosten für die Provision beteiligt. Eine Regelung nach dem Besteller Prinzip, nach dem immer die Partei zahlt, die den Immobilienmakler beauftragt hat, ist künftig unzulässig."""

        if dictionary["gesetz"] == "1":
            dictionary["gesetz"] = text
            dictionary["gesetz1"] = text1
        else:
            dictionary["gesetz"] = ""
            dictionary["gesetz1"] = ""



    ''' Load the data and save the columns with categories as a dataframe. 
    This section also allows changes in the numerical and categorical columns. '''
    if st.button("Load Data"):
        st.write(dictionary)
