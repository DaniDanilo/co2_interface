import gradio as gr
from interface.input_processing import clean_and_match
from interface.calculation import calculate_emissions
from config import reference_db, result_column, sentence_transformers_model, emissions_source_name, emissions_source, left_on, right_on, excel_output_path

def run_interface(merged_categories):
     def pipeline(input):
          matching_outputs =  clean_and_match(result_column, input, reference_db, merged_categories, sentence_transformers_model)
          carbon_footprint, max_emission_product = calculate_emissions(emissions_source_name,
                                                                      emissions_source, matching_outputs, left_on, right_on, excel_output_path)
          return carbon_footprint, max_emission_product

     demo = gr.Interface(fn=pipeline,
                         inputs=gr.Dataframe(
                              headers=['Food item', 'Amount of Food (kg)', 'Country Code'],
                              datatype=['str', 'number','str'],
                              label='Enter the products to calculate CO2 for:'
                              ),
                         outputs=[
                              gr.outputs.Textbox(label="Total Carbon Footprint (kg CO2-eq/kg)"),
                              gr.outputs.Textbox(label="Biggest Contributor for Emissions")
                         ],
                         title="Find the carbon footprint of your desired food items")
     demo.launch(share=True)  