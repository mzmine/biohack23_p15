from matchms import filtering as msfilters

PRIMARY_FILTERS = [
    "make_charge_int",
    "interpret_pepmass",
    "harmonize_undefined_inchikey",
    "harmonize_undefined_inchi",
    "harmonize_undefined_smiles",
    "add_retention_time",
    "add_retention_index",    
    "add_compound_name"
]

REPAIR_FILTERS = [
    "derive_ionmode",
    "correct_charge",
    "derive_adduct_from_name",
    "derive_formula_from_name",
    "clean_compound_name",
    "add_precursor_mz",
    "add_parent_mass",
    "repair_inchi_inchikey_smiles",
    "derive_smiles_from_inchi",
    "derive_inchi_from_smiles",
    "derive_inchikey_from_inchi",
    "clean_adduct",
    "derive_smiles_from_pubchem_compound_name_search",
    "repair_smiles_of_salts",
    "repair_precursor_is_parent_mass",
    "repair_parent_mass_is_mol_wt",
    "repair_adduct_based_on_smiles",
    "repair_parent_mass_match_smiles_wrapper",
    "repair_not_matching_annotation"
]

VALIDATION_FILTERS = [
    "require_precursor_mz",
    "require_valid_annotation",
    "require_correct_ionmode",
    "require_parent_mass_match_smiles"
]
