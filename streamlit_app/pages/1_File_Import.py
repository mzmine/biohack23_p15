import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide", 
    page_title="File Import - FAIR MS Library Curation Editor", 
    #page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://github.com/mzmine/biohack23_p15',
        'Report a bug': "https://github.com/mzmine/biohack23_p15/issues/new/choose",
        'About': "# This is the creation and curation wizard for FAIR MS Libraries."
    }
)

st.markdown("## File Import")
st.markdown("Please select an Excel file to upload. The file should contain one or more sheets. Each sheet should contain sample columns, detailing factors of each individual sample (rows). Lipid identities are the column headers of the non-sample columns, quantities should be reported in the cells.")

uploaded_file = st.file_uploader("Choose a file", )
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
        
        xl = pd.ExcelFile(uploaded_file)
        sheets = xl.sheet_names
        for sheet in sheets:
            if sheet not in datasets:
                df = pd.read_excel(uploaded_file, sheet_name=sheet)
                datasets[sheet] = df

        st.markdown("## Preview Sheets")
        sheet_selector = st.selectbox(
                "Select a sheet",
                sheets
            )
        if sheet_selector is not None and sheet_selector in datasets:
            rowsMetricColumn, columnsMetricColumn = st.columns(2)
            with rowsMetricColumn:
                st.metric('Rows', datasets[sheet_selector].shape[0])
            with columnsMetricColumn:
                st.metric('Columns', datasets[sheet_selector].shape[1])
            st.write(datasets[sheet_selector])

        st.markdown("## Select Sheets as Datasets")
        selected_sheets = st.multiselect(
            'Each selected sheet will be converted to a dataset',
            sheets,
            sheets
        )
        st.session_state['datasets'] = datasets
        st.session_state['selected_sheets'] = selected_sheets

        if 'datasets' not in st.session_state:
            st.session_state['datasets'] = []
