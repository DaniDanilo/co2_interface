import gradio as gr
from input_processing import match

demo = gr.Interface(fn=match,
                    inputs=[gr.Textbox(label='Food item', placeholder='Be as specific as possible'),
                            gr.Number(label='Amount of food in kilograms'),
                            gr.Textbox(label='Country Code', placeholder='Please only write a country code, not a name')
                        ],
                    
                    outputs=[gr.outputs.Textbox(label="Product Type"),
                             gr.outputs.Textbox(label="Carbon Footprint (kg CO2-eq/kg)"),
                             gr.outputs.Textbox(label="Country Code")
                        ],
                    title="Find the carbon footprint of your desired food item")
demo.launch()  