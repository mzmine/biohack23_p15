"""Code for running the validation pipeline.
Includes repairing and validating.
Repairs should be documented in a computer readable way

Require correct metadata filters output None if the requirement is not passed, we also need to store which filter was not passed.
Repair functions, just change the metadata, so we can check for changes that occured.

Add index handling - when a spectrum is processed, its id is added to the corresponding list
"""

class ValidationPipeline:

    def __init__(self, spectrum) -> None:
        pass

    def run(spectrum):
        #here run all the checks and modifications
        return modifications #{'quality':, 'metadata adduct': {'previous':..., 'updated':....}}