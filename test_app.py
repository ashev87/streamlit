from io import BytesIO
from docxtpl import DocxTemplate
import pandas as pd
from mailmerge import MailMerge
import fitz
import streamlit as st
from PIL import Image
from base64 import b64decode
from tempfile import TemporaryFile

def read_excel(file_name):
    """Reads the excel file and returns a dictionary with the data"""
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
    return dictionary

def read_docx(file_name):
    """ Reads a docx file and switches the template fields with the values from the dictionary """
    document = MailMerge(file_word)
    print('Die Mergefelder werden ersetzt...')
    document.merge(date=str(dictionary['Datum'].strftime("%d. %B %Y")),
                anrede=dictionary['Anrede'],
                geehrter=dictionary['Geehrter'],
                vorname=dictionary['Vorname'],
                nachname=dictionary['Nachname'],
                email=dictionary['Email'],
                ansprechpartner=dictionary['Ansprechpartner'],
                ansprechpartner_email=dictionary['Ansprechpartner_Email'],
                ansprechpartner_mobil=dictionary['Ansprechpartner_Mobil'],
                ansprechpartner_position=dictionary['Ansprechpartner_Position'],
                street=dictionary['Strasse'],
                artikel_adresse=str(dictionary['Artikel_Adresse']),
                HausNr=str(dictionary['HausNr']),
                plz=str(dictionary['PLZ']),
                bezirk=str(dictionary['Bezirk']),
                city=dictionary['Stadt'],
                pricefrom=str('{:,}'.format(dictionary['Preis_von'])).replace(',', '.'),
                priceto=str('{:,}'.format(dictionary['Preis_bis'])).replace(',', '.'),
                datum_besichtigung=str(dictionary['Datum_Besichtigung'].strftime("%d.%m.%Y")),
                titel=str(dictionary['Objekt_Titel']),
                artikel_objekttyp=str(dictionary['Artikel_Objekttyp']),
                baujahr=str(dictionary['Baujahr']),
                ausstattungsmerkmale=dictionary['Ausstattungsmerkmale'],
                fenster=dictionary['Fenster'],
                boden=dictionary['Boden'],
                # terrasse=dictionary['Terrasse'],
                ausrichtung=dictionary['Ausrichtung'],
                pkw_stellplatz=dictionary['PKW_Stellplatz'],
                # besonderheit=dictionary['Besonderheit'],
                heizung=dictionary['Heizung'],
                energietraeger=dictionary['Energieträger'],
                keller=dictionary['Keller'],
                dach=dictionary['Dach'],
                vermietungssituation=dictionary['Vermietungssituation'],
                wohngeld=str(dictionary['Wohngeld']),
                barrierfreiheit=str(dictionary['Barrierfrei']),
                letzte_modernisierung=str(dictionary['Letzte_Modernisierung']),
                was=str(dictionary['was']),
                etage=str(dictionary['etage']),
                etagenzahl=str(dictionary['etagenzahl']),
                aufzug_vorhanden=str(dictionary['aufzug vorhanden']),
                anzahl_bad=str(dictionary['anzahl bad']),
                gaste_wc=str(dictionary['gaste wc']),
                wc_ausstattung=str(dictionary['wc_ausstattung']),
                jahr_kueche=str(dictionary['jahr_kueche']),
                wert_kueche=str(dictionary['wert_kueche']),
                zimmer_anzahl=str(dictionary['zimmer_anzahl']),
                # grundstuckgrosse=str('{:,}'.format(dictionary['Grundstuckgrosse']).replace(',', '.')),
                grundstuckgrosse=str(dictionary['Grundstuckgrosse']),
                wohnflaeche=str(dictionary['wohnflaeche']),
                bodenrichtwert_m2=str(dictionary['bodenrichtwert_m2']),
                # balkon_terrase_m2=str(dictionary['Balkon_flaeche']),
                anzahl_balkon=str(dictionary['anzahl_balkon']),
                flaesche_balkon=str(dictionary['flaesche_balkon']),
                anzahl_terrase=str(dictionary['anzahl_terrase']),
                flaesche_terrase=str(dictionary['flaesche_terrase']),
                garten=str(dictionary['Garten_flaeche']),
                gerauschbelastung=dictionary['Gerauschbelastung'],
                symbol_larm=str(dictionary['Symbol_Larm']),
                symbol_immo=str(dictionary['Immobilie_Symbol']),
                vorteil1=str(dictionary['Vorteil1']),
                vorteil2=str(dictionary['Vorteil2']),
                vorteil3=str(dictionary['Vorteil3']),
                vorteil4=str(dictionary['Vorteil4']),
                vorteil5=str(dictionary['Vorteil5']),
                nachteil1=str(dictionary['Nachteil1']),
                nachteil2=str(dictionary['Nachteil2']),
                nachteil3=str(dictionary['Nachteil3']),
                nachteil4=str(dictionary['Nachteil4']),
                nachteil5=str(dictionary['Nachteil5']),
                qualitaet_fassade=dictionary['Qualität_Fassade'],
                qualitaet_hauseingang=dictionary['Qualität_Hauseingang'],
                qualitaet_treppenhaus=dictionary['Qualität_Treppenhaus'],
                qualitaet_sanitar=dictionary['Qualität_Sanitär'],
                qualitaet_boden=dictionary['Qualität_Boden'],
                qualitaet_terrasse=dictionary['Qualität_Terrasse'],
                qualitaet_garten=dictionary['Qualität_Garten'],
                qualitaet_keller=dictionary['Qualität_Keller'],
                qualitaet_fenster=dictionary['Qualität_Fenster'],
                qualitaet_dach=dictionary['Qualität_Dach'],
                qualitaet_elektrik=dictionary['Qualität_Elektrik'],
                qualitaet_heizung=dictionary['Qualität_Heizung'],
                qualitaet_straenge=dictionary['Qualität_Straenge'],
                qualitaet_kueche=dictionary['Qualität_Küche'],
                zustand_fassade=dictionary['Zustand_Fassade'],
                zustand_hauseingang=dictionary['Zustand_Hauseingang'],
                zustand_treppenhaus=dictionary['Zustand_Treppenhaus'],
                zustand_sanitar=dictionary['Zustand_Sanitär'],
                zustand_boden=dictionary['Zustand_Boden'],
                zustand_terrasse=dictionary['Zustand_Terrasse'],
                zustand_garten=dictionary['Zustand_Garten'],
                zustand_keller=dictionary['Zustand_Keller'],
                zustand_fenster=dictionary['Zustand_Fenster'],
                zustand_dach=dictionary['Zustand_Dach'],
                zustand_elektrik=dictionary['Zustand_Elektrik'],
                zustand_heizung=dictionary['Zustand_Heizung'],
                zustand_straenge=dictionary['Zustand_Straenge'],
                zustand_kueche=dictionary['Zustand_Küche'],
                resume1=dictionary['Resume1'],
                resume2=dictionary['Resume2']+dictionary['Resume2_erw'],
                resume3=dictionary['Resume3'],
                objekttyp=str(dictionary['Objekttyp']),
                m2_price_from=str('{:,}'.format(int(dictionary['m2_Preis_von'])).replace(',', '.')),
                m2_price_to=str('{:,}'.format(int(dictionary['m2_Preis_bis'])).replace(',', '.')),
                angebot_price=str('{:,}'.format(dictionary['Angebot_Preis']).replace(',', '.')),
                m2_angebot=str('{:,}'.format(int(dictionary['m2_Angebot'])).replace(',', '.')),
                monaten=str(dictionary['monaten']),
                die_immobilie=dictionary['Die_Immobilie'],
                die_immobilie2=dictionary['Die_Immobilie2'],
                gesetz=dictionary['gesetz'],
                gesetz1=dictionary['gesetz1']
                )
    dest_file = "MWA.docx"
    document.write(dest_file)
    return dest_file
    
def create_image_buffer_from_pdf_page(page_object):
    """
    Create a buffer from a pdf page object.
    """
    zoom = 3.5
    mat = fitz.Matrix(zoom, zoom)
    pix = page_object.get_pixmap(matrix = mat)
    img = Image.frombytes("RGB", \
                         [pix.width, pix.height], \
                         pix.samples)
    buffer = TemporaryFile()            # create a buffer
    img.save(buffer, format="PNG")	# save to buffer
    buffer.seek(0)	                # return to the start of the buffer
    return buffer

def read_pdf(file_name, pictures):
    """ Reads a pdf file adds the pages to the pictures list and returns the pictures list """
    doc = fitz.open(stream=file_name.read(), filetype="pdf")
    print("Die Seiten von Pricehubble werden gespriechert")
    vergleichsobjekte_page = doc.load_page(8)  # number of page
    nahversorgung_page = doc.load_page(20)  # number of page
    erreichbarkeit_page = doc.load_page(21)  # number of page
    bauvorhaben_page = doc.load_page(22)  # number of page
    pictures['vergleichsobjekte_page'] = create_image_buffer_from_pdf_page(vergleichsobjekte_page)
    pictures['erreichbarkeit_page'] = create_image_buffer_from_pdf_page(erreichbarkeit_page)
    pictures['bauvorhaben_page'] = create_image_buffer_from_pdf_page(bauvorhaben_page)
    pictures['nahversorgung_page'] = create_image_buffer_from_pdf_page(nahversorgung_page)
    return pictures

def read_pictures(uploaded_files, pictures):
    """Assigns the uploaded files to the pictures dictionary"""
    for uploaded_file in uploaded_files:
        if uploaded_file.name == '1.jpg' or uploaded_file.name == '1.png':
            jpg_1 = uploaded_file
            pictures['jpg_1'] = jpg_1
        elif uploaded_file.name == '2.jpg' or uploaded_file.name == '2.png':
            jpg_2 = uploaded_file
            pictures['jpg_2'] = jpg_2
        elif uploaded_file.name == '3.jpg' or uploaded_file.name == '3.png':
            jpg_3 = uploaded_file
            pictures['jpg_3'] = jpg_3
        elif uploaded_file.name == '4.jpg' or uploaded_file.name == '4.png':
            jpg_4 = uploaded_file
            pictures['jpg_4'] = jpg_4
        elif uploaded_file.name == '5.jpg' or uploaded_file.name == '5.png':
            jpg_5 = uploaded_file
            pictures['jpg_5'] = jpg_5
        elif uploaded_file.name == '6.jpg' or uploaded_file.name == '6.png':
            jpg_6 = uploaded_file
            pictures['jpg_6'] = jpg_6
        elif uploaded_file.name == '7.jpg' or uploaded_file.name == '7.png':
            jpg_7 = uploaded_file
            pictures['jpg_7'] = jpg_7
        elif uploaded_file.name == '8.jpg' or uploaded_file.name == '8.png':
            jpg_8 = uploaded_file
            pictures['jpg_8'] = jpg_8
        elif uploaded_file.name == '9.jpg' or uploaded_file.name == '9.png':
            jpg_9 = uploaded_file
            pictures['jpg_9'] = jpg_9
        elif uploaded_file.name == '10.jpg' or uploaded_file.name == '10.png':
            jpg_10 = uploaded_file
            pictures['jpg_10'] = jpg_10
        elif uploaded_file.name == '11.jpg' or uploaded_file.name == '11.png':
            jpg_11 = uploaded_file
            pictures['jpg_11'] = jpg_11
        elif uploaded_file.name == '12.jpg' or uploaded_file.name == '12.png':
            jpg_12 = uploaded_file
            pictures['jpg_12'] = jpg_12
        elif uploaded_file.name == 'deckseite.png':
            jpg_deckseite = uploaded_file
            pictures['jpg_deckseite'] = jpg_deckseite
        elif uploaded_file.name == 'maps.png':
            png_maps = uploaded_file
            pictures['png_maps'] = png_maps
        elif uploaded_file.name == 'flur.png':
            png_flur = uploaded_file
            pictures['png_flur'] = png_flur
        elif uploaded_file.name == 'larm.png':
            png_larm = uploaded_file
            pictures['png_larm'] = png_larm
        else:
            print("Photo name not correct")
    return pictures

def change_pictures():
    """ Change the pictures in the template """
    tpl.replace_pic('deckseite.png', pictures['jpg_deckseite'])
    tpl.replace_pic('picture1', pictures['jpg_1'])
    tpl.replace_pic('picture2', pictures['jpg_2'])
    tpl.replace_pic('picture3', pictures['jpg_3'])
    tpl.replace_pic('picture4', pictures['jpg_4'])
    tpl.replace_pic('picture5', pictures['jpg_5'])
    tpl.replace_pic('picture6', pictures['jpg_6'])
    tpl.replace_pic('picture7', pictures['jpg_7'])
    tpl.replace_pic('picture8', pictures['jpg_8'])
    tpl.replace_pic('picture9', pictures['jpg_9'])
    tpl.replace_pic('picture10', pictures['jpg_10'])
    tpl.replace_pic('picture11', pictures['jpg_11'])
    tpl.replace_pic('picture12', pictures['jpg_12'])
    tpl.replace_pic('maps', pictures['png_maps'])
    tpl.replace_pic('flur', pictures['png_flur'])
    tpl.replace_pic('larm', pictures['png_larm'])
    tpl.replace_pic('Grafik 25', pictures['nahversorgung_page'])
    tpl.replace_pic('Grafik 55', pictures['erreichbarkeit_page'])
    tpl.replace_pic('Grafik 82', pictures['bauvorhaben_page'])
    tpl.replace_pic('Grafik 58', pictures['vergleichsobjekte_page'])

# Logo and Title
image = Image.open('dk-logo-black.png')
st.title("DK - Cool MWA Tool")
st.write("Creating an MWA the cool way!")
# initaite a dictionary to store the pictures
pictures = {}
# upload 2 files 
file_excel = st.file_uploader("Upload Excel",type=['xlsx'])
if file_excel is not None:
    dictionary = read_excel(file_excel)
    st.success("Erfolgreich Excel hochgeladen")
    # save_uploaded_file(file_excel)
    # st.write(dictionary)
file_word = st.file_uploader("Upload Word file",type=['docx'])
if file_word is not None:
    dest_file = read_docx(file_word)
    st.success("Erfolgreich MWA Template hochgeladen")

pricehubble_file = st.file_uploader("Upload PriceHubble file",type=['pdf'])
if pricehubble_file is not None:
    pictures = read_pdf(pricehubble_file, pictures)
    st.success("Erfolgreich Pricehubble hochgeladen")

label = """The pictures must be with the following names: 1.jpg or 1.png, etc.
    deckseteite.png, maps.png, flur.png, larm.png"""
uploaded_files = st.file_uploader(label, accept_multiple_files=True)
if len(uploaded_files) > 0:
    pictures = read_pictures(uploaded_files, pictures)
    tpl = DocxTemplate(dest_file)
    context = {}
    change_pictures()
    tpl.render(context)
    dest_file2 = BytesIO()
    #dest_file2.write(tpl.save("dest_file2.docx"))
    tpl.save(dest_file2)
    #dest_file2.seek(0)
    st.success("MWA erfolgreich erstellt")
    btn = st.download_button(
        label="Press to download the MWA",
        data=dest_file2,
        file_name="MWA.docx",
        mime="application/octet-stream"
    )