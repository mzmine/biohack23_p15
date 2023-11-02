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
    #uploaded_file = st.session_state['uploaded_file']
    with st.spinner('Loading data...'):
        datasets = {}
        if 'datasets' in st.session_state:
            datasets = st.session_state['datasets']
        else:
            st.session_state['datasets'] = datasets

    with NamedTemporaryFile(dir='.', suffix='.mgf', mode = "wb") as f:
        f.write(uploaded_file.getbuffer())
        f.close()
        spectra_temp = load_from_mgf(f.name) 
        #spectra_temp = load_from_mgf(uploaded_file, "wb")
        spectra = list(spectra_temp)
        df_spectra = pd.DataFrame({"spectrum": spectra})

        
        # make dataframe for metadata
        def extract_metadata(df, keys):
            for key in keys:
                df[key] = df["spectrum"].apply(lambda x: x.get(key))


        extract_metadata(df_spectra, df_spectra["spectrum"][0].metadata.keys())

        st.markdown("## Preview Information")

        st.metric('Detected how many spectra', len(df_spectra))

        st.write(df_spectra)

     
        st.session_state['df_spectra'] = df_spectra
        st.session_state['len_spectra'] = len(df_spectra)

        if 'df_spectra' not in st.session_state:
            st.session_state['df_spectra'] = []
