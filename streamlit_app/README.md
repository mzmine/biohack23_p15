# Streamlit Application for FAIR MassSpectral Library Curation and Editing

[GitHub repository](https://github.com/mzmine/biohack23_p15) - folder _streamlit_app_

## Installation

## Development

Use python venv to use defined dependencies.

    python -m venv venv
    source venv/bin/activate


### windows
	1. cd C:/Users/rfm848
	2. python -m venv venv
	3. .\venv\Scripts\activate.bat
	4. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser 
    5. .\venv\Scripts\activate.ps1


to activate the virtual environment.

You can then use the provided requirements.txt to populate the required dependencies in your virtual environment.

    pip install -r requirements.txt

## Running the application

After you have activated the virtual environment and the packages listed in requirements.txt are installed, you can launch the streamlit application as follows:

    streamlit run FAIR_MS_Library_Editor.py 
