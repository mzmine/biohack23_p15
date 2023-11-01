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

    def update_spectra_quality_lists(self, spectrum_id):
        """Will update validated_spectra and nonvalidated_spectra list for this spectrum_id"""
        valid_spectrum = True
        if len(self.failed_requirements[spectrum_id]) != 0:
            valid_spectrum = False
        for modification in self.modifications[spectrum_id]:
            if modification.validated_by_user is False:
                valid_spectrum = False

        if valid_spectrum is True:
            self.validated_spectra.append(spectrum_id)
            if spectrum_id in self.nonvalidated_spectra:
                self.nonvalidated_spectra.remove(spectrum_id)
        else:
            self.nonvalidated_spectra.append(spectrum_id)
            if spectrum_id in self.nonvalidated_spectra:
                self.nonvalidated_spectra.remove(spectrum_id)

    def pass_user_validation_info(self, spectrum_id):
        '''
        This function is called only for nonvalidated spectra
        '''
        assert spectrum_id in self.nonvalidated_spectra

        modifications = self.modifications[spectrum_id]
        failed_requirements = self.failed_requirements[spectrum_id]

        return modifications, failed_requirements, self.spectra[spectrum_id]
    
    def user_approve_repair(self, field_name, approved_all: bool, rejected_all: bool, spectrum_id):
        '''
        This function allows user to accept or decline all or part of modifications
        '''
        modifications = self.modifications[spectrum_id]
        if approved_all:
            for modification in modifications:
                if modification.metadata_field == field_name:
                    # self.modifications[spectrum_id].pop(modification) #todo test this!!
                    self.modifications[spectrum_id].validated_by_user = True
        #if user rejects the changes
        #todo implement the case when user rejects not all changes
        elif rejected_all:
            for modification in modifications:
                #todo should we use before/original/first modification
                self.spectra[spectrum_id].get(modification.metadata_field).set(modification.before)
            modifications.pop(spectrum_id)
            self.failed_requirements[spectrum_id] = self.spectrum_validator.process_spectrum_store_failed_filters(self.spectra[spectrum_id])
            self.update_spectra_lists(spectrum_id)
        else: 
            #todo implement!!!!
            #only the last one
            return None

    
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

    def initial_run(self):
        #first check
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

    
        