from docxtpl import DocxTemplate
from pathlib import Path
import os
import pandas as pd
from mailmerge import MailMerge
import locale
import fitz
import zipfile
import streamlit as st

def save_uploaded_file(uploadedfile):
    makeDir()
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

def checkDir():
	if 'tempDir' in os.listdir('../'): 
		return True
	return False

def makeDir():
	if checkDir(): 
		pass
	else: 
		os.mkdir('../tempDir')

# upload 2 files 
file_excel = st.file_uploader("Upload Excel",type=['xlsx'])
if file_excel is not None:
    df = pd.read_excel(file_excel, sheet_name='script', header=None, names=['keys', 'values'], na_values='(None)', usecols = 'A:B')
    df = df.fillna('')
    keys = df['keys'].tolist()
    values = df['values'].tolist()
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
    # save_uploaded_file(file_excel)
    st.write(dictionary)
    
# print(dictionary["gesetz"])
#DEST_FILE = 'MWA_2.docx'