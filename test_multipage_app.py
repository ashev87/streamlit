import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import homepage, page1 # import your pages here

# Create an instance of the app 
app = MultiPage()
# Add all your applications (pages) here
app.add_page("Homepage", homepage.app)
app.add_page("Page1", page1.app)
# The main app
app.run()