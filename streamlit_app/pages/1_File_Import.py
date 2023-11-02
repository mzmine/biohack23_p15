from library_spectra_validation.library_handler import LibraryHandler
import os

import streamlit as st
import pandas as pd
from matchms.importing import load_from_mgf
from tempfile import NamedTemporaryFile


st.set_page_config(
    layout="wide", 
    page_title="File Import (.mgf) - FAIR MS Library Curation Editor", 
    #page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://github.com/mzmine/biohack23_p15',
        'Report a bug': "https://github.com/mzmine/biohack23_p15/issues/new/choose",
        'About': "# This is the creation and curation wizard for FAIR MS Libraries."
    }
)

st.markdown("## File Import (.mgf)")
st.markdown("Please select an mgf to upload.")

uploaded_file = st.file_uploader("Choose a file", type = ".mgf")
st.set_option('deprecation.showfileUploaderEncoding', False)
    


if uploaded_file is not None:
    print(uploaded_file)
    st.session_state['uploaded_file'] = uploaded_file

if 'uploaded_file' in st.session_state and st.session_state['uploaded_file'] is not None:
    print("Uploaded file:", st.session_state['uploaded_file'])
    uploaded_file = st.session_state['uploaded_file']
    with st.spinner('Loading data...'):
        datasets = {}
        if 'datasets' in st.session_state:
            datasets = st.session_state['datasets']
        else:
            st.session_state['datasets'] = datasets

    mgf_file = os.path.join(st.session_state['working_dir'], uploaded_file.name)

    with open(file=mgf_file, mode="wb") as f:
        f.write(uploaded_file.getbuffer())

    # load spectra from mgf, TODO: replace with SpectralLibrary implementation and import
    # we will receive a list of spectra metadata (each being a dataframe)
    # TODO: we can retrieve each spectrum from the SpectralLibrary object
    # TODO: display forward and backward buttons to page through spectra

    lib_handler = LibraryHandler(f.name)

    spectra_temp = load_from_mgf(f.name)
    spectra = list(spectra_temp)
    df_spectra = pd.DataFrame({"spectrum": spectra})
        
    # make dataframe for metadata
    def extract_metadata(df, keys):
        for key in keys:
            df[key] = df["spectrum"].apply(lambda x: x.get(key))


    extract_metadata(df_spectra, df_spectra["spectrum"][0].metadata.keys())

    st.markdown("## Preview Information")

    st.metric('Detected how many spectra', len(df_spectra))

    st.data_editor(df_spectra)# , on_change=user_metadata_change())


    st.session_state['spectra'] = spectra
    st.session_state['df_spectra'] = df_spectra
    st.session_state['len_spectra'] = len(df_spectra)

    if 'df_spectra' not in st.session_state:
        st.session_state['df_spectra'] = []
