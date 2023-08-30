from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import re

def match_codex_and_exei(sentence_transformers_model,codexfilename, exeifilename, columns_to_use, output_file):
    #Getting the data from codex and filtered Ex to Ei
    df1=pd.read_excel(codexfilename).astype(str)
    df2=pd.read_excel(exeifilename ,usecols=columns_to_use)

    #Creating function for making sure that capitalization does not affect matching
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    #Combining L1 through L6 rows from codex
    df1['Merged'] = df1.apply(lambda row: f"{row['L1']} {row['L2']} {row['L3']} {row['L4']} {row['L5']} {row['L6']} {row['Product Title'].lower()}", axis=1)
    #Cleaning text and making merged column into a list
    df1['Merged']=df1['Merged'].apply(clean_text)
    codex = df1['Merged'].to_list()

    #Combining Product Type and Hiot names from Ex to Ei file
    df2['Exei']=df2.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
    df2['Exei']=df2['Exei'].apply(clean_text)
    exei = df2['Exei'].to_list()

    # Creating model for embedding our data
    model = SentenceTransformer(sentence_transformers_model)

    #Compute embedding for merged product names of Ex to Ei
    embeddings1 = model.encode(exei, convert_to_tensor=True)

    product_matches = []  # List to store the matched merged values for each product.

    #Embedding each merged row of codex and matching it with merged Ex to Ei product names
    ## this will be useful for when we calculate CO2
    for codex_product in codex:
        cosine_score = util.cos_sim(embeddings1, model.encode(codex_product))
        best_match_index = np.argmax(cosine_score)
        exei_matches=exei[best_match_index]
        product_matches.append((codex_product, exei_matches))

    # Create a new DataFrame to store the matches
    matches_df = pd.DataFrame(product_matches, columns=['Merged', 'Matched Category'])

    # Add disected columns from original codex
    matches_df = matches_df.join(df1[['Product Title', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6']])

    # Save the matches to an Excel file
    matches_df.to_excel(output_file, index=False)