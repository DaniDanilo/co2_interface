from interface.generate_matching import match_codex_and_exei
from interface.process_sueatable import prep_sueatable
from interface.category_embedding import create_reference_db
from interface.app import run_interface
from config import sentence_transformers_model, emissions_source_name, columnname, reference_db

def create_merged_resource(resource_name):
    #if you want to use the manually updated categories file, use the "merged_apporach_manual" file
    if resource_name == "manual":
        output_file = "outputs/merged_approach_manual.xlsx"    
    elif resource_name == "exei":
        codex_filename = "resources/ClearCO2_dataset.xlsx"
        #it should have at least following columns: "Product Title", "L1", "L2", "L3", "L4", "L5", "L6"
        exei_filename = "resources/food_related_emissions.xlsx"
        columns_to_use = ["ProductTypeName_of_hiot", "ProductTypeName"]
        output_file = "outputs/merged_approach_All.xlsx"
        match_codex_and_exei(sentence_transformers_model, codex_filename, exei_filename, columns_to_use, output_file)
    elif resource_name == "sueatable":
        sueatable_filename = "resources/SuEatableLife.xlsx"
        output_file = "outputs/merged_sueatable.xlsx"
        prep_sueatable(sueatable_filename, output_file)
    return output_file


merged_categories = create_merged_resource(emissions_source_name)

create_reference_db(merged_categories, columnname, reference_db, sentence_transformers_model) #take codex file and export numerical embeddings  

run_interface(merged_categories)

