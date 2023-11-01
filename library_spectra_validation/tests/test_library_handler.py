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
