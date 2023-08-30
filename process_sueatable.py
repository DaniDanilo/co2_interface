import pandas as pd
import re
def prep_sueatable(sueatable_filename, output_file):
     #Getting the data
    df = pd.read_excel(sueatable_filename).astype(str)

    #Creating function for making sure that capitalization does not affect matching
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    #Combining L1 through L6 rows from codex
    df['Merged'] = df.apply(lambda row: f"{row['FOOD COMMODITY GROUP']} {row['Food commodity ITEM']} {row['Typology']} {row['Description']}", axis=1)
    #Cleaning text and making merged column into a list
    df['Merged']=df['Merged'].apply(clean_text)
    df.to_excel(output_file)