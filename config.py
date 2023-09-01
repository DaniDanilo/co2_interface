sentence_transformers_model = "paraphrase-MiniLM-L6-v2"
#pick "exei", "manual", or "sueatable"
emissions_source_name = "sueatable"
emissions_source = "resources/SuEatableLife.xlsx"
columnname = "Merged"
reference_db = "outputs/ref_db.npy"
result_column = "Food commodity ITEM"
left_on = ["Matched Category"]
right_on = ["Food commodity ITEM"]
excel_output_path = "interface_outputs/matched_outputs"
