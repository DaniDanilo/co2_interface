
# pip install sentence_transformers

import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

#Reading the Ex to Ei file that includes CO2 emissions,
#the macthed file of Codex and Ex to Ei products and the Google Form answers
df1=pd.read_excel('resources/food_related_emissions.xlsx', usecols=['ProductTypeName_of_hiot', 'ProductTypeName', 'CountryCode', 'CarbonFootprint','unit'])
df2=pd.read_excel('outputs/merged_approach_All.xlsx', usecols=['Codex Merged Input', 'Matched Category'])
df3=pd.read_excel('google_forms/user_input.xlsx', usecols=['Category of goods:',
                                              'If you can specify the product/s: (Ex. Chocolate milk)',
                                              'If the goods are imported from outside Austria, please specify the country.',
                                              'Amount of acquired food in Kilograms:'])

#Function to make sure capitalization does not affect our matching process
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

#Processing data for use
df1["Exei"]=df1.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
df1['Exei']=df1['Exei'].apply(clean_text)
emissions_data_df=df1

exei= df2['Codex Merged Input'].tolist()

#Creating model for embedding our data
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#Embedding every codex product from the matched document (df2)
embeddings_exei = model.encode(exei, convert_to_tensor=True)

#If the products have not been imported, then they have been produced in Austria
country_column = 'If the goods are imported from outside Austria, please specify the country.'
df3[country_column].fillna("AT", inplace=True) # Fill empty cells in the specified country column with "AT"

df3['Input']=df3.apply(lambda row: f"{row['Category of goods:']} {row['If you can specify the product/s: (Ex. Chocolate milk)']}", axis=1)
df3['Input']=df3['Input'].apply(clean_text)
user_input = df3['Input'].tolist()

product_matches = []  # List to store the matched Merged values for each product.

#Embedding each user-inputed product and matching it merged codex embeddings
for input in user_input:
    input_embedding = model.encode(input, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(input_embedding, embeddings_exei)[0]
    best_match_index = cosine_scores.argmax()
    best_match_index = int(best_match_index)
    exei_matches = df2.loc[best_match_index]

     #Making sure to add not only the matched Codex product but also the corresponding Ex to Ei parent category match
    product_matches.append((input, exei_matches['Codex Merged Input'], exei_matches['Matched Category']))

# Create a new DataFrame to store the matches
matched_results_df = pd.DataFrame(product_matches, columns=['User Input', 'Codex','Ex to Ei'])

#Adding the user-inputed country and amount of food into the data frame
matched_results_df=matched_results_df.join(df3[['If the goods are imported from outside Austria, please specify the country.',
                             'Amount of acquired food in Kilograms:']], rsuffix='_df3')

#Merge emissions data with matched results based on category and country
merged_data = pd.merge(matched_results_df, emissions_data_df,
                       how="left", left_on=['Ex to Ei', 'If the goods are imported from outside Austria, please specify the country.'],
                       right_on=["Exei", "CountryCode"])

# Calculate CO2 emissions based on user kg and emissions per kg
merged_data["Total CO2 Emissions"] = merged_data["Amount of acquired food in Kilograms:"] * merged_data["CarbonFootprint"]

# Update the matched_results_df with the calculated emissions
matched_results_df["Total CO2 Emissions"] = merged_data["Total CO2 Emissions"]

# Save the updated matched_results_df to a new Excel file
matched_results_df.to_excel("google_forms/outputs/matched_results_with_emissions.xlsx", index=False)