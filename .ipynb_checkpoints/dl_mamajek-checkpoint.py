import pandas as pd
import numpy as np
from astropy.io import ascii
import requests

def dl_mamajek(save_path="mamajek.csv"):
    mamajek_url = 'https://raw.githubusercontent.com/emamajek/SpectralType/refs/heads/master/EEM_dwarf_UBVIJHK_colors_Teff.txt'
    mamajek_response = requests.get(mamajek_url)
    lines = mamajek_response.text.splitlines()

    trim_indices = []

    for index, value in enumerate(lines):
        if '#SpT' in value:
            trim_indices.append(index) 

    original_response = lines[trim_indices[0]:trim_indices[1]] 
    response_copy = original_response[:] 
    
    for i in range(0, len(response_copy)): 
        response_copy[i] = response_copy[i].replace(':', ' ') 
        response_copy[i] = response_copy[i].replace('#', '') 
    
    for index in range(len(response_copy)):
        data_list = list(filter(None, response_copy[index].split()))
        for i in range(len(data_list)): 
            if '...' in data_list[i]:
                data_list[i] = 'null'
        response_copy[index] = data_list
        
    single_space_copy = response_copy[:]
    for i in range(len(single_space_copy)):
        joined = " ".join(single_space_copy[i]) ##join the list of words (one row) into a single string, separated by a single space
        single_space_copy[i] = joined ##replaces the content of table_response[i] with the newly-joined string
    
    mamajek_data_table = ascii.read(single_space_copy, format='basic', delimiter=' ', fill_values=[('null', np.nan)]) ##turn into ascii table
    
    mamajek_df = mamajek_data_table.to_pandas() ##redefine dataframe from ascii table
    mamajek_df['M_H'] = round(mamajek_df['H-Ks'] + mamajek_df['M_Ks'], 3)
    mamajek_df['M_V'] = round(mamajek_df['V-Ks'] + mamajek_df['M_Ks'], 3)
    mamajek_df['M_Rp'] = round(mamajek_df['M_G'] - mamajek_df['G-Rp'], 3)
    mamajek_df['M_W1'] = round(mamajek_df['M_Ks'] - mamajek_df['Ks-W1'], 3)
    mamajek_df['M_B'] = round(mamajek_df['B-V'] + mamajek_df['M_V'], 3)
    mamajek_df['M_Bp'] = round(mamajek_df['Bp-Rp'] + mamajek_df['M_Rp'], 3)
    mamajek_df['M_Rc'] = round(mamajek_df['M_V'] - mamajek_df['V-Rc'], 3)
    mamajek_df['M_Ic'] = round(mamajek_df['M_V'] - mamajek_df['V-Ic'], 3)
    mamajek_df['M_W2'] = round(mamajek_df['M_W1'] - mamajek_df['W1-W2'], 3)
    mamajek_df['M_W3'] = round(mamajek_df['M_W1'] - mamajek_df['W1-W3'], 3)
    mamajek_df['M_W4'] = round(mamajek_df['M_W1'] - mamajek_df['W1-W4'], 3)
    mamajek_df['M_U'] = round(mamajek_df['U-B'] + mamajek_df['M_B'], 3)
    mamajek_df.drop(columns='SpT_1', inplace=True)

    mamajek_df.to_csv(save_path, index=False)

if __name__ == "__main__":
    dl_mamajek()


## To run script: python dl_mamajek.py