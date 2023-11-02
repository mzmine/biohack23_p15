"""Code for running the validation pipeline.
Includes repairing and validating.
Repairs should be documented in a computer readable way

Require correct metadata filters output None if the requirement is not passed, we also need to store which filter was not passed.
Repair functions, just change the metadata, so we can check for changes that occured.

Add index handling - when a spectrum is processed, its id is added to the corresponding list
"""

import logging
from typing import Iterable, List, Optional, Union, Tuple
from matchms.filtering.SpectrumProcessor import SpectrumProcessor
from matchms import Spectrum

logger = logging.getLogger("matchms")

METADATA_FIELDS_OF_INTEREST = ["parent_mass", "precursor_mz", "adduct", "smiles",
                                "compound_name", "inchi", "inchikey", "charge", "ionmode"]

class Modification:
    def __init__(self, metadata_field, before, after, logging_message, validated_by_user):
        self.metadata_field = metadata_field
        self.before = before
        self.after = after
        self.logging_message = logging_message
        self.validated_by_user = validated_by_user


class RequirementFailure:
    def __init__(self, metadata_field, logging_message):
        self.metadata_field = metadata_field
        self.logging_message = logging_message       


def find_modifications(spectrum_old, spectrum_new, logging_message: str):
    """Checks which modifications have been made in a filter step"""
    modifications = []
    for metadata_field in METADATA_FIELDS_OF_INTEREST:
        if spectrum_old.get(metadata_field) != spectrum_new.get(metadata_field):
            modifications.append(
                Modification(metadata_field=metadata_field,
                             before=spectrum_old.get(metadata_field),
                             after=spectrum_new.get(metadata_field),
                             logging_message=logging_message,
                             validated_by_user=False))
    return modifications


class SpectrumRepairer(SpectrumProcessor):
    def __init__(self, predefined_pipeline: Optional[str] = 'default',
                 additional_filters: Iterable[Union[str, List[dict]]] = ()):
        super().__init__(predefined_pipeline,
                         additional_filters)

    def process_spectrum(self, spectrum,
                         processing_report=None):
        raise AttributeError("process spectrum is not a valid method of SpectrumValidator")

    def process_spectrum_store_modifications(self, spectrum) -> Tuple[List[Modification], Spectrum]:
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
            if spectrum_out is None:
                raise AttributeError("SpectrumRepairer is only expected to repair spectra, not set to None")
            spectrum = spectrum_out
        return modifications, spectrum


class SpectrumValidator(SpectrumProcessor):
    def __init__(self):
        self.fields_checked_by_filter = {
            "require_precursor_mz": ["precursor_mz"],
            "require_valid_annotation": ["smiles", "inchi", "inchikey"],
            "require_correct_ionmode": ["ionmode", "adduct", "charge"],
            # "require_parent_mass_match_smiles": ["smiles", "parent_mass"]
        }
        # todo require adduct, precursor mz and parent mass match.
        # todo add all the checks for formatting. That everything is filled and of the expected format.
        super().__init__(predefined_pipeline=None,
                         additional_filters=("require_precursor_mz",
                                             "require_valid_annotation",
                                             ("require_correct_ionmode", {"ion_mode_to_keep": "both"}),
                                             # ("require_parent_mass_match_smiles", {'mass_tolerance': 0.1}),
                                             ))
        # todo add require parent mass match smiles after matchms release.
    def process_spectrum(self, spectrum,
                         processing_report=None):
        raise AttributeError("process spectrum is not a valid method of SpectrumValidator")

    def process_spectrum_store_failed_filters(self, spectrum) -> List[RequirementFailure]:
        if not self.filters:
            raise TypeError("No filters to process")
        failed_requirements = []
        for filter_func in self.filters:
            # todo capture logging
            logging_message = ""
            spectrum_out = filter_func(spectrum)
            if spectrum_out is None:
                fields_changed = self.fields_checked_by_filter[filter_func.__name__]
                for field_changed in fields_changed:
                    failed_requirements.append(RequirementFailure(field_changed,
                                                                  logging_message))
        return failed_requirements
