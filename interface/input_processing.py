import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

#making sure capitalization does not affect matching
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

#making sure country code will be capitalized
def uppercase(text):
    text = text.upper()
    text = re.sub(r'[^A-Z0-9\s]', '', text)
    return text

def match(input, amount, country_code):
    input=clean_text(input)
    country_code=uppercase(country_code)

    model=SentenceTransformer('paraphrase-MiniLM-L6-v2')
    input_embedding=model.encode(input)

    ref_db = np.load('outputs/ref_db.npy')
    categories=pd.read_excel('outputs/merged_approach_manual.xlsx')

    outputs= []
    cosine_scores = util.pytorch_cos_sim(input_embedding, ref_db)[0]
    best_match_index = cosine_scores.argmax()
    best_match_index = int(best_match_index)
    exei_matches = categories.loc[best_match_index]

    outputs.append((input, exei_matches['Matched Category'], country_code, amount))
    outputs_df=pd.DataFrame(outputs, columns=['Input', 'Matched Category', 'Country', 'Amount'])

    emissions_data=pd.read_excel('food_related_emissions.xlsx')
    emissions_data["Exei"]=emissions_data.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
    emissions_data['Exei']=emissions_data['Exei'].apply(clean_text)
    emissions_data_df=emissions_data

    #Merging df based on same category and country code
    merged_data = pd.merge(outputs_df, emissions_data_df,
                       how="left", left_on=['Matched Category', 'Country'],
                       right_on=["Exei", "CountryCode"])
    
    # Calculate CO2 emissions based on user kg and emissions per kg
    merged_data["Total CO2 Emissions"] = merged_data["Amount"] * merged_data["CarbonFootprint"]

    # Update the matched_results_df with the calculated emissions
    outputs_df["Total CO2 Emissions"] = merged_data["Total CO2 Emissions"]

    #extracting needed outputs
    product_type = outputs_df['Matched Category']
    carbon_footprint = outputs_df['Total CO2 Emissions']
    country_code = outputs_df['Country']

    return product_type, carbon_footprint, country_code
