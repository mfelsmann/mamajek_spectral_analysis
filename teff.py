import numpy as np
import pandas as pd
import sys
import os
from dl_exo import dl_exofop

def load_exo_df_from_file(path='exofop.csv'):
    return pd.read_csv(path)

def get_teff(id_tag, exo_df=None, path='exofop.csv'):
    if exo_df is None:
        if not os.path.exists(path):
            dl_exofop(path)  # Import, download, format, and save the ExoFOP database
        exo_df = load_exo_df_from_file(path) # Load local copy of ExoFOP database to pandas DataFrame
    tag_length = len(str(int(id_tag)))
    if tag_length <= 5:
        toi_formatted = f"{int(id_tag)}.01"
        index = exo_df[exo_df.iloc[:, 1] == float(toi_formatted)].index
        if index.empty:
            raise ValueError(f"No matching target entry found in database")
        
    else:
        tic = f"{int(id_tag)}"
        index = exo_df[exo_df.iloc[:, 0] == float(tic)].index
        if index.empty: 
            raise ValueError(f"No matching target entry found in database")

    index_value = index[0] # First instance of match
    teff = exo_df.loc[index_value, 'Stellar Eff Temp (K)']
    if not pd.notna(teff) or teff == '':
        raise ValueError(f"Target has no temperature entry in database")
    teff_unc_raw = exo_df.loc[index_value, 'Stellar Eff Temp (K) err']
    teff_unc = teff_unc_raw if pd.notna(teff_unc_raw) and teff_unc_raw != '' else 0

    return { "teff": teff, 
            "unc": teff_unc
           }

if __name__ == "__main__":
    id_tag = sys.argv[1]
    # exo_df = load_exo_df_from_file()
    result = get_teff(id_tag)
    print(result)

## To run script: python teff.py tag_number
    ## EX: python teff.py 7011
    ## Should return: {'teff': 5493.0, 'teff_unc': 140.6}