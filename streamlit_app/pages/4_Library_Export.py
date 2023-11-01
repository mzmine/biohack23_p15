import streamlit as st

st.set_page_config(
    layout="wide", 
    page_title="Library Export - FAIR MS Library Curation Editor", 
    #page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://github.com/mzmine/biohack23_p15',
        'Report a bug': "https://github.com/mzmine/biohack23_p15/issues/new/choose",
        'About': "# This is the creation and curation wizard for FAIR MS Libraries."
    }
)

st.markdown("## Conversion to MS Library Export Format")

datasets = {}
if 'datasets' in st.session_state:
    datasets = st.session_state['datasets']

metadata_parts = {}
if 'metadata_parts' in st.session_state:
    metadata_parts = st.session_state['metadata_parts']

with st.form("conversion-settings", clear_on_submit=False):
    if datasets == {}:
        st.warning("Please upload a file to begin!")
    
    if metadata_parts == {}:
        st.warning("Please enter metadata to begin!")
    
    submit_disabled = (metadata_parts == {} or datasets == {})
    convert = st.form_submit_button("Create MS Library XYZ file", disabled=submit_disabled)
    if convert:
        st.info("Exporting to XYZ format...")
