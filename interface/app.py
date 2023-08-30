import gradio as gr
from input_processing import match

demo = gr.Interface(fn=match,
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
demo.launch()  