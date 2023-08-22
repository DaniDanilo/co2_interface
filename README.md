# CO2_matching_model

### Folders:

1. google_forms: the solution for loading user input from google forms output xlsx file into the model. Gives matching to a codex category & respective ex_ei row with CO2 emissions calculated for the weight of the product entered.
2. interface: interactive webpage hosted on hugginface spaces that allows endusers directly enter the product of interest into the input field and obtain the CO2 emission values on the webpage in real time with no excel files involved from users' side.

### Files in google_forms:

1. #### [generate_matching.py](google_forms/generate_matching.py)

   Performs semantic cosine similarity matching between the product titles and L1-L6 category columns of the ClearKarma allergen food classification database(ClearCO2_dataset.xlsx) and the food related rows of the ecoinvent-exiobase database taken from a research publication at [https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.13271](https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.13271) (food_related_emissions.xlsx)

   Steps taken in the process:


   1. Load the two datasets from excel files, merge columns L1 through L6 in the [ClearCO2_dataset.xlsx](resources/ClearCO2_dataset.xlsx) to obtain a context sentence for each food item(category name/subcategory etc), clean the texts to conform tp the same format; merge Product Type and Product Type Hiot fields from the [food_related_emissions.xlsx](resources/food_related_emissions.xlsx) file to obtain context sentences for the product categories that we have emissions data for.
   2. Using SentenceTransformer('All-MiniLM-L6-v2') create numerical embedddings for the context sentences from the emissions dataset and save it for future reference.
   3. iterate through the ClearCO2_dataset.xlsx to find a most probable match (based on cosine similarity of the embeddings of the product row and ex_ei row) for each product in the set.
   4. obtain results file where each row represents data from the allergen food classification list and has an additional field of the matched category from the available food emissions list
2. #### [CO2_lookup_for_googleforms.py](google_forms/CO2_lookup_for_googleforms.py)


   1. Create numerical embeddings for the previously matched outputs(containg product title, L1-L6 categories + ecoinvent-exiobase category)
   2. For each user input row in the google forms output table, perform a matching between the emissions/categories contexts file and the input sentence
   3. Merge the emissions file with the matched categories file to combine the information like selected country and product weight  with its emission factors
   4. Output final CO2 emissions value to google_forms/outputs/matched_results_with_emissions.xlsx

### Files in interface:

1. [app.py](interface/app.py)
	Create a web page that contains an interactive form using Gradio plugin. Hosted via hugginface spaces at[https://huggingface.co/spaces/DaniloH/co2_calculation](https://huggingface.co/spaces/DaniloH/co2_calculation)

The web app is up and available to the users 24/7 due to cloud hosting. The interface callse the "match" python function from the input-processing.py file on click of the submit button. The functionality can also be accesed through API calls, which may be useful for the other web applications we are building that use carbon emissions data.

2. [input_processing.py](interface/input_processing.py) utilizes the numerical embeddings created by category_embedding.py(Run it first before anything else!), so that we do not embed the same file every time a user submits a request. This way, we only embed the users input text and then run against the per made embeddings to find a match(similar to the google forms approach), then return the emissions values to the interface
3. [category_embedding.py](interface/category_embedding.py) creates numerical embeddings for the Codex+Matched ecoinvent-exiobase merged file(combination of product title, L1-L6, Product Type name and Product Hiot type name) and exports it for later use in the interface as ref_db.npy

### Files:


1. [codex/ClearCO2_dataset.xlsx](resources/ClearCO2_dataset.xlsx) - data base created by ClearKarma with over 4000 categories of food and especifications for them
2. [food_related_emissions.xlsx](resources/food_related_emissions.xlsx) - Ex to Ei products containing the respective CO2 emission per kg of food data, taking intoa ccount also the country of origin
3. [user_input.xlsx](google_forms/user_input.xlsx) - answers from the Google Form containing product category, especification, country, amount (kg), among others
4. [merged_approach_All.xlsx](outputs/merged_approach_All.xlsx) - matched result table between Ex to Ei and Codex products using 'All-MiniLM-L6-v2' model
5. [matched_results_with_emissions.xlsx](outputs/matched_results_with_emissions.xlsx) - matched user input with Codex product and the respective CO2 emission of the products with 'All-MiniLM-L6-v2' model
6. [ref_db.npy](resources/ref_db.npy) - output embeddings to be used in interface
7. [requirements.txt](requirements.txt) - everything needed for interface to work properly
