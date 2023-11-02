from matchms.plotting.spectrum_plots import plot_spectra_mirror, plot_spectrum
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pubchempy
from rdkit import Chem
from rdkit.Chem import Draw




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


st.markdown("## Plot selected MS2 spectrum")
st.markdown("Please select a spectrum based on compound_name")


spectra = st.session_state['spectra'] 
df_spectra = st.session_state['df_spectra']

cmp_list = df_spectra["compound_name"].tolist()

st.markdown("## Select a compound name")
cmp_selector = st.selectbox(
    "select a compound name",
    cmp_list
)

if cmp_selector in cmp_list:
    cmp_id = cmp_list.index(cmp_selector)
    cmp_smile = df_spectra.loc[cmp_id]["smiles"]


    plt_spectrum = spectra[cmp_id]

    fig, axs = plt.subplots(1, 2, figsize=(12.8, 4.2), gridspec_kw={'width_ratios': [2, 5]}, sharey=False)
    cmp_img = Chem.Draw.MolToImage(Chem.MolFromSmiles(cmp_smile), ax=axs[0])

    axs[0].grid(False)
    axs[0].tick_params(axis='both', bottom=False, labelbottom=False, left=False, labelleft=False)
    axs[0].set_title(cmp_smile)
    axs[0].imshow(cmp_img)
    axs[0].axis("off")

    plot_spectrum(plt_spectrum, axs[1])

    st.pyplot(fig)