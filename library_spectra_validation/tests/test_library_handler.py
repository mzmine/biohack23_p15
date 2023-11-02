from library_handler import LibraryHandler


def test_init_library_handler():
    LibraryHandler("./examples/test_case_correct.mgf")


def test_approve_repairs():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    library_handler.approve_repair(spectrum_id=spectrum_id, field_name="inchi")
    assert library_handler.modifications[spectrum_id][0].validated_by_user is True


def test_approve_all_repairs():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    library_handler.approve_all_repairs(spectrum_id=spectrum_id)
    for modification in library_handler.modifications[spectrum_id]:
        assert modification.validated_by_user is True


def test_decline_last_repairs():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    library_handler.decline_last_repair(spectrum_id=spectrum_id, field_name="inchi")
    assert len(library_handler.modifications[0]) == 1


def test_decline_all_repairs_on_a_field():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    # todo add test that actually has multiple repairs for one field
    library_handler.decline_all_repairs_on_a_field(spectrum_id=spectrum_id, field_name="inchi")
    assert len(library_handler.modifications[0]) == 1


def test_decline_all_repairs_spectrum():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    library_handler.decline_all_repairs_spectrum(spectrum_id=spectrum_id)
    assert len(library_handler.modifications[0]) == 0

    # todo check that change is undone


def test_decline_wrapper():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    original_spectrum = library_handler.spectra[0]
    spectrum_id = 0
    library_handler.decline_wrapper(spectrum_id=spectrum_id, field_name=None, only_last_repair=False)
    assert len(library_handler.modifications[0]) == 0
    # check that changes were undone
    assert original_spectrum == library_handler.spectra[spectrum_id]
    assert len(library_handler.failed_requirements[spectrum_id]) == 3
    assert spectrum_id in library_handler.nonvalidated_spectra


def test_user_metadata_change():
    library_handler = LibraryHandler("./examples/test_case_correct.mgf")
    spectrum_id = 0
    library_handler.user_metadata_change(spectrum_id=spectrum_id, field_name="smiles", user_input="CCC")
    assert library_handler.spectra[spectrum_id].get("smiles") == "CCC"
