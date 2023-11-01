from library_spectra_validation.library_handler import LibraryHandler

def test_load_spectra():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
