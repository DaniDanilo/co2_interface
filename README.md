---
title: CO2_calculator
app_file: main.py
sdk: gradio
sdk_version: 3.40.1
---
# CO2_matching_model

### Starting Point:

1. [config](config.py) : configure the parameters for the interface to run, this will be used throughout the rest of files.
   
   -sentence_transformer_model: what model from sentence-transformers library to be used
   
   -emissions_source_name: either use "manual", "exei" or "sueatable" in order to choose which data base of food related emissions to use
   
   -emissions_source: the path for obtaining the food related emissions data base
   
   -columnname: the column that contains the categories to be embedded for matching with input
   
   -reference_db: path for the file obtained when embedding categories from food related emissions file
   
   -result_column: column that has the main item from emissions file (and not the merged version)
   
   -left_on: column name from the outputs_df to be merged with emissions file
   
   -right_on: column name from the emissions file to be merged with outputs_df
   		*the columns that both data frames have in common
   
   -excel_ouput_path: path where the results from matching and CO2 calculations will be stored
   
3. [main](main.py) : main file to run interface and all other files needed.
   
### Folders:
1. interface: interactive webpage hosted on hugginface spaces that allows endusers directly enter the product of interest into the input field and obtain the CO2 emission values on the webpage in real time with no excel files involved from users' side.
2. interface_outputs: excel files with time stamp with the matching information of the interface inputs. Can be used to check for discrepancies of matching or simply as a control of how many times the interface has been used

### Files in interface:

1. [app.py](interface/app.py)
	Create a web page that contains an interactive form using Gradio plugin. Hosted via hugginface spaces at[https://huggingface.co/spaces/TeamCarrot/CO2_calculator](https://huggingface.co/spaces/TeamCarrot/CO2_calculator)

The web app is up and available to the users 24/7 due to cloud hosting. The interface calls the pipeline from the function "run_interface" when clicking of the submit button. The functionality can also be accesed through API calls, which may be useful for the other web applications we are building that use carbon emissions data.

2. [input_processing.py](interface/input_processing.py) utilizes the numerical embeddings created by category_embedding.py(Run it first before anything else!), so that we do not embed the same file every time a user submits a request. This way, we only embed the users input text and then run against the per made embeddings to find a match, then return the emissions values to the interface
3. [category_embedding.py](interface/category_embedding.py) creates numerical embeddings for the base emissions file chosen and exports it for later use in the interface as ref_db.npy
4. [calculation](interface/calculation.py) calculates the total emissions for all products and gives the interface the needed outputs of total emissions, the products that emmits the most CO2, as well as a list of the matched categories from our data base.

### Files:


1. [codex/ClearCO2_dataset.xlsx](resources/ClearCO2_dataset.xlsx) - data base created by ClearKarma with over 4000 categories of food and especifications for them
2. [food_related_emissions.xlsx](resources/food_related_emissions.xlsx) - Ex to Ei products containing the respective CO2 emission per kg of food data, taking intoa ccount also the country of origin
3. [user_input.xlsx](google_forms/user_input.xlsx) - answers from the Google Form containing product category, especification, country, amount (kg), among others
4. [merged_approach_All.xlsx](outputs/merged_approach_All.xlsx) - matched result table between Ex to Ei and Codex products using 'All-MiniLM-L6-v2' model
5. [matched_results_with_emissions.xlsx](outputs/matched_results_with_emissions.xlsx) - matched user input with Codex product and the respective CO2 emission of the products with 'All-MiniLM-L6-v2' model
6. [ref_db.npy](resources/ref_db.npy) - output embeddings to be used in interface
7. [requirements.txt](requirements.txt) - everything needed for interface to work properly
