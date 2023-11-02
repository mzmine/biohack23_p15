from matchms.importing import load_spectra
from matchms.filtering.SpectrumProcessor import SpectrumProcessor
from filters import PRIMARY_FILTERS
from validation_pipeline import Modification, SpectrumRepairer, SpectrumValidator

class LibraryHandler:
    """Stores the 3 different types of spectra. Correct, repaired, wrong.
    Has internal organization using spectrum ids"""

    def __init__(self, f):
        metadata_field_harmonization = SpectrumProcessor(predefined_pipeline=None,
                                                         additional_filters=PRIMARY_FILTERS)
        self.spectra = metadata_field_harmonization.process_spectrums(load_spectra(f))
        self.spectrum_repairer = SpectrumRepairer()
        self.spectrum_validator = SpectrumValidator()
        self.validated_spectra = []
        self.nonvalidated_spectra = []
        self.modifications = {} 
        self.failed_requirements = {}

        self.initial_run()

    def initial_run(self):
        for spectrum_id in range(len(self.spectra)):
            spectrum = self.spectra[spectrum_id]
            modifications, spectrum = self.spectrum_repairer.process_spectrum_store_modifications(spectrum)
            self.modifications[spectrum_id] = modifications

            self.failed_requirements[spectrum_id] = self.spectrum_validator.process_spectrum_store_failed_filters(
                spectrum)
            self.update_spectra_quality_lists(spectrum_id)
            self.spectra[spectrum_id] = spectrum

        # iterate over all failed requirements
        # it's almost streamlit
        # for the dashboard run should use spectrum id
        # for spectrum_id in range(len(self.spectra)):
        #     if len(self.failed_requirements[spectrum_id]) != 0:
        #         self.pass_user_validation_info(spectrum_id)
        #         #todo should we grab here state variable from streamlit - accept or change
        #         # self.user_approve_repair(spectrum_id)
        #         # self.user_metadat_change(spectrum_id)

    def update_spectra_quality_lists(self, spectrum_id):
        """Will update validated_spectra and nonvalidated_spectra list for this spectrum_id"""
        valid_spectrum = True
        if len(self.failed_requirements[spectrum_id]) != 0:
            valid_spectrum = False
        for modification in self.modifications[spectrum_id]:
            if modification.validated_by_user is False:
                valid_spectrum = False

        if valid_spectrum is True:
            if spectrum_id not in self.validated_spectra:
                self.validated_spectra.append(spectrum_id)
            if spectrum_id in self.nonvalidated_spectra:
                self.nonvalidated_spectra.remove(spectrum_id)
        else:
            if spectrum_id not in self.nonvalidated_spectra:
                self.nonvalidated_spectra.append(spectrum_id)
            if spectrum_id in self.validated_spectra:
                self.validated_spectra.remove(spectrum_id)

    def return_user_validation_info(self, spectrum_id):
        '''
        Returns all info related to spectrum_id
        '''
        assert spectrum_id in self.nonvalidated_spectra

        modifications = self.modifications[spectrum_id]
        failed_requirements = self.failed_requirements[spectrum_id]

        return modifications, failed_requirements, self.spectra[spectrum_id]

    def approve_repair(self, spectrum_id, field_name):
        """Accepts every modification done to a field_name"""
        # Accepts every modification so far.
        for modification in self.modifications[spectrum_id]:
            if modification.metadata_field == field_name:
                modification.validated_by_user = True
        self.update_spectra_quality_lists(spectrum_id)

    def approve_all_repairs(self, spectrum_id):
        """Accepts all modifications done for a spectrum"""
        for modification in self.modifications[spectrum_id]:
            modification.validated_by_user = True
        self.update_spectra_quality_lists(spectrum_id)

    def decline_last_repair(self, spectrum_id, field_name):
        """Undo the last modification made to a field"""
        for mod_idx, modification in enumerate(self.modifications[spectrum_id]):
            # Checks if it is the correct metadata field and if it was the last changed made
            if modification.metadata_field == field_name and modification.after == self.spectra[spectrum_id].get(field_name):
                # undo change
                spectrum = self.spectra[spectrum_id]
                spectrum.set(field_name, modification.before)
                self.spectra[spectrum_id] = spectrum
                # remove the modification from the list of modifications
                del self.modifications[spectrum_id][mod_idx]
                # todo run validation after.

    def decline_all_repairs_on_a_field(self, spectrum_id, field_name):
        """Undoes all the repairs for a specific field.

        This is achieved by iteratively removing the last added repair"""
        nr_of_modifications_to_field = len([modification for modification in self.modifications[spectrum_id]
                                            if modification.metadata_field == field_name])
        # Removes all the modifications until the last one was removed.
        for _ in range(nr_of_modifications_to_field):
            self.decline_last_repair(spectrum_id, field_name)
            # todo run validation after.

    def decline_all_repairs_spectrum(self, spectrum_id):
        """Undoes all modifications made to a spectrum"""
        while len(self.modifications[spectrum_id]) > 0:
            for mod_idx, modification in enumerate(self.modifications[spectrum_id]):
                field_name = modification.metadata_field
                # Checks if it was the last changed made
                if modification.after == self.spectra[spectrum_id].get(field_name):
                    # undo change
                    spectrum = self.spectra[spectrum_id]
                    spectrum.set(field_name, modification.before)
                    self.spectra[spectrum_id] = spectrum
                    # remove the modification from the list of modifications
                    del self.modifications[spectrum_id][mod_idx]

    def decline_wrapper(self, spectrum_id, field_name, only_last_repair: bool):
        if field_name is None:
            self.decline_all_repairs_spectrum(spectrum_id)
        elif only_last_repair:
            self.decline_last_repair(spectrum_id, field_name)
        else:
            self.decline_all_repairs_on_a_field(spectrum_id, field_name)

        self.failed_requirements[spectrum_id] = self.spectrum_validator.process_spectrum_store_failed_filters(self.spectra[spectrum_id])
        self.update_spectra_quality_lists(spectrum_id)

    def user_metadata_change(self, field_name, user_input, spectrum_id):
        '''
        This function takes user defined metadata and rewrites the required field in spectra
        The info on user-defined modifications is added to modifications dictionary and mandatory 
        validation is rerun.
        '''
        self.spectra[spectrum_id].set(field_name, user_input) #todo this is correct, fix everywhere
        #todo add user-defined modification to modifications list
        self.modifications[spectrum_id].append("User-defined modification in the field " +
                                               field_name + 
                                               ". Value changed to " +
                                               user_input)
        self.failed_requirements[spectrum_id] = self.spectrum_validator.process_spectrum_store_failed_filters(self.spectra[spectrum_id])

    def user_rerun_repair(self, spectrum_id, rerun: bool):
        '''
        The function behind user's choice to rerun the repairment and validation
        Should be linked to a button in a dashboard
        '''
        if rerun: #todo do we even need it??
            self.modifications[spectrum_id] = self.spectrum_repairer.process_spectrum_store_modifications(self.spectra[spectrum_id])
            self.failed_requirements[spectrum_id] = self.spectrum_validator.process_spectrum_store_failed_filters(self.spectra[spectrum_id])


    
        