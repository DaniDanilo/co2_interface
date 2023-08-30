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

def clean_and_match(result_column, input, reference_db, merged_categories, sentence_transformers_model):
    products = input['Food item']
    country_code = input['Country Code']
    amount = input['Amount of Food (kg)']

    ref_db = np.load(reference_db)
    categories = pd.read_excel(merged_categories)

    outputs = []
    model = SentenceTransformer(sentence_transformers_model)

    for product, cc, amount in zip(products, country_code, amount):  # Loop through both products and country codes
        product = clean_text(product)
        cc = uppercase(cc) 
        input_embedding = model.encode(product)

        cosine_scores = util.pytorch_cos_sim(input_embedding, ref_db)[0]
        best_match_index = cosine_scores.argmax()
        best_match_index = int(best_match_index)
        result = categories.loc[best_match_index]
        print(product, result[result_column], cc, amount)
        outputs.append((product, result[result_column], cc, amount))

    outputs_df = pd.DataFrame(outputs, columns=['Input', 'Matched Category', 'Country', 'Amount'])
    return outputs_df
   

