"""Code for running the validation pipeline.
Includes repairing and validating.
Repairs should be documented in a computer readable way

Require correct metadata filters output None if the requirement is not passed, we also need to store which filter was not passed.
Repair functions, just change the metadata, so we can check for changes that occured.

Add index handling - when a spectrum is processed, its id is added to the corresponding list
"""

import logging
from typing import Iterable, List, Optional, Union
from matchms.filtering.SpectrumProcessor import SpectrumProcessor

logger = logging.getLogger("matchms")


class Modification:
    def __init__(self, metadata_field, before, after, logging_message, validated_by_user):
        self.metadata_field = metadata_field
        self.before = before
        self.after = after
        self.logging_message = logging_message
        self.validated_by_user = validated_by_user


def find_modifications(spectrum_old, spectrum_new, logging_message: str):
    """Checks which modifications have been made in a filter step"""
    modifications = []
    metadata_fields_to_check = ["parent_mass", "precursor_mz", "adduct", "smiles",
                                "compound_name", "inchi", "inchikey", "charge", "ionmode"]
    for metadata_field in metadata_fields_to_check:
        if spectrum_old.get(metadata_field) != spectrum_new.get(metadata_field):
            modifications.append(
                Modification(metadata_field=metadata_field,
                             before=spectrum_old.get(metadata_field),
                             after=spectrum_new(metadata_field),
                             logging_message=logging_message,
                             validated_by_user=False))
    return modifications


class SpectrumValidator(SpectrumProcessor):
    def __init__(self, predefined_pipeline: Optional[str] = 'default',
                 additional_filters: Iterable[Union[str, List[dict]]] = ()):
        super().__init__(predefined_pipeline,
                         additional_filters)

    def process_spectrum(self, spectrum,
                         processing_report=None):
        raise AttributeError("process spectrum is not a valid method of SpectrumValidator")

    def process_spectrum_store_modifications(self, spectrum) -> List[Modification]:
        if not self.filters:
            raise TypeError("No filters to process")
        modifications = []
        for filter_func in self.filters:
            # todo capture logging
            logging_message = ""
            spectrum_out = filter_func(spectrum)
            modifications += find_modifications(spectrum_old=spectrum,
                                                spectrum_new=spectrum_out,
                                                logging_message=logging_message)
            # todo Think about what to do here
            if spectrum_out is None:
                break
            spectrum = spectrum_out
        return modifications
