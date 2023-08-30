import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def uppercase(text):
    text = text.upper()
    text = re.sub(r'[^A-Z0-9\s]', '', text)
    return text

def match(input):
    products = input['Food item']
    country_code = input['Country Code']
    amount = input['Amount of Food (kg)']

    ref_db = np.load('ref_db.npy')
    categories = pd.read_excel('merged_approach_paraphrase.xlsx')

<<<<<<< HEAD
    outputs = []
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
=======
    ref_db = np.load('outputs/ref_db.npy')
    categories=pd.read_excel('outputs/merged_approach_manual.xlsx')
>>>>>>> c3f5960f36b4e7471522dfd812ab4fb8982d291b

    for product, cc, amount in zip(products, country_code, amount):  # Loop through both products and country codes
        product = clean_text(product)
        cc = uppercase(cc) 

        input_embedding = model.encode(product)

        cosine_scores = util.pytorch_cos_sim(input_embedding, ref_db)[0]
        best_match_index = cosine_scores.argmax()
        best_match_index = int(best_match_index)
        exei_matches = categories.loc[best_match_index]

        outputs.append((product, exei_matches['Matched Category'], cc, amount))

    outputs_df = pd.DataFrame(outputs, columns=['Input', 'Matched Category', 'Country', 'Amount'])

    emissions_data = pd.read_excel('food_related_emissions.xlsx')
    emissions_data["Exei"] = emissions_data.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
    emissions_data['Exei'] = emissions_data['Exei'].apply(clean_text)
    emissions_data_df = emissions_data 

    merged_data = pd.merge(outputs_df, emissions_data_df,
                           how="left", left_on=['Matched Category', 'Country'],
                           right_on=["Exei", "CountryCode"])

    merged_data["Amount"] = merged_data["Amount"].astype(float)
    merged_data["CarbonFootprint"] = merged_data["CarbonFootprint"].astype(float)

    
    merged_data["Total CO2 Emissions"] = merged_data["Amount"] * merged_data["CarbonFootprint"]

    outputs_df["Total CO2 Emissions"] = merged_data["Total CO2 Emissions"]

    carbon_footprint = outputs_df['Total CO2 Emissions'].sum()
    max_emission_product = outputs_df.loc[outputs_df['Total CO2 Emissions'].idxmax(), 'Input'] 

    return carbon_footprint, max_emission_product

