import pandas as pd
import re
# merged_data = pd.merge(outputs_df, emissions_data_df,
#                        how="left", left_on=['Matched Category', 'Country'],
#                        right_on=["Exei", "CountryCode"])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def prep_exei(emissions_data_raw):
    emissions_data_raw["Exei"] = emissions_data_raw.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
    emissions_data_raw["Exei"] = emissions_data_raw['Exei'].apply(clean_text)
    emissions_data_df = emissions_data_raw 
    return emissions_data_df

def calculate_emissions(emissions_source_name, emissions_source, matching_outputs, left_on, right_on):
    outputs_df = matching_outputs
    emissions_data = pd.read_excel(emissions_source)
    if(emissions_source_name == "exei"):
        emissions_data = prep_exei(emissions_data, outputs_df)

    merged_data = pd.merge(outputs_df, emissions_data,
                           how="left", left_on=left_on,
                           right_on=right_on)
    
    merged_data["Amount"] = merged_data["Amount"].astype(float)
    merged_data["CarbonFootprint"] = merged_data["CarbonFootprint"].astype(float)

    
    merged_data["Total CO2 Emissions"] = merged_data["Amount"] * merged_data["CarbonFootprint"]

    outputs_df["Total CO2 Emissions"] = merged_data["Total CO2 Emissions"]

    carbon_footprint = outputs_df['Total CO2 Emissions'].sum()
    max_emission_product = outputs_df.loc[outputs_df['Total CO2 Emissions'].idxmax(), 'Input'] 

    return carbon_footprint, max_emission_product