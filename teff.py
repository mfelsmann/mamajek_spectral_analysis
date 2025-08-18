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
        exo_df = load_exo_df_from_file(path)
    tag_length = len(str(int(id_tag)))
    if tag_length <= 5:
        toi_formatted = f"{int(id_tag)}.01"
        index = exo_df[exo_df.iloc[:, 1] == float(toi_formatted)].index
        if index.empty:
            raise ValueError(f"No matching target entry found in database")
        index_value=index[0]
        teff = exo_df.loc[index_value, 'Stellar Eff Temp (K)']
        if not pd.notna(teff) or teff == '':
            raise ValueError(f"Target has no temperature entry in database")
        teff_unc_raw = exo_df.loc[index_value, 'Stellar Eff Temp (K) err']
        teff_unc = teff_unc_raw if pd.notna(teff_unc_raw) and teff_unc_raw != '' else 0
        
    else:
        tic = f"{int(id_tag)}"
        index = exo_df[exo_df.iloc[:, 0] == float(tic)].index
        if index.empty:
            from astroquery.exceptions import ResolverError
            from astroquery.mast import Catalogs
            target_name = f"TIC {tic}"
            try:
                catalogTIC = Catalogs.query_object(target_name, radius=0.002, catalog="TIC")
            except ResolverError:
                raise ValueError(f"No matching entry found in database")
            filtered = catalogTIC[catalogTIC['ID'] == f'{tic}']
            teff = filtered['Teff'][0]
            teff_unc_raw = filtered['e_Teff'][0]
            teff_unc = teff_unc_raw if pd.notna(teff_unc_raw) and teff_unc_raw != '' else 0
        else:
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
    result = get_teff(id_tag)
    print(result)
