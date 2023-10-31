from matchms.importing import load_spectra

class LibraryHandler:
    """Stores the 3 different types of spetra. Correct, repaired, wrong.
    Has internal organization using spectrum ids"""

    def __init__(self, f, pipeline):
        self.spectra = load_spectra(f)
        self.pipeline = pipeline
        
        self.spectra_dictionary = {
            'valid': None, #[id1, id2,...]
            'repaired': None, #[id1:[modifications],..]
            'invalid': None #also a dictionary
        }
        self.modifications = []

    def clean_and_validate_spectrum(spectrum_id):
        spectrum = self.spectra[spectrum_id]
        modifications = self.pipeline.run(spectrum)
        self.spectra_dictionary[modifications.spectra_quality].append(spectrum_id) #vcalid, repired,...
        self.modifications.append(modifications)

    def run():
        for spectrum in self.spectra:
            clean_and_validate(spectrum)