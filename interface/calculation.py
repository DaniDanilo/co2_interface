import pandas as pd
import re
import os
from datetime import datetime

# merged_data = pd.merge(outputs_df, emissions_data_df,
#                        how="left", left_on=['Matched Category', 'Country'],
#                        right_on=["Exei", "CountryCode"])

#function to make sure capitalization does not affect matching
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

#having the correct column from Ex to Ei data base to be matched later
def prep_exei(emissions_data_raw):
    emissions_data_raw["Exei"] = emissions_data_raw.apply(lambda row: f"{row['ProductTypeName_of_hiot']} {row['ProductTypeName']}", axis=1)
    emissions_data_raw["Exei"] = emissions_data_raw['Exei'].apply(clean_text)
    emissions_data_df = emissions_data_raw 
    return emissions_data_df

#getting the emissions from the inputed products
def calculate_emissions(emissions_source_name, emissions_source, matching_outputs, left_on, right_on, excel_output_path):
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

    # Generate a unique filename based on timestamp and identifier
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    while True:
        unique_filename = f"{excel_output_path}_{timestamp}.xlsx"
        if not os.path.exists(unique_filename):
            break

    # Saving the Excel file with the generated unique filename
    outputs_df.to_excel(unique_filename)

    # Getting the needed outputs to be displayed in interface
    carbon_footprint = outputs_df['Total CO2 Emissions'].sum()
    max_emission_product = outputs_df.loc[outputs_df['Total CO2 Emissions'].idxmax(), 'Input'] 
    matchings = "\n".join(outputs_df["Matched Category"].astype(str))

    return carbon_footprint, max_emission_product, matchings