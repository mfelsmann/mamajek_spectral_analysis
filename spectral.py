import pandas as pd
import numpy as np
import argparse
import os
from dl_mamajek import dl_mamajek_table

def load_mamajek_from_file(path='mamajek.csv'):
    return pd.read_csv(path)

def spectral_type(teff, teff_unc, filter, d_mag, dm_unc, mamajek_df=None, path='mamajek.csv'):
    if mamajek_df is None:
        if not os.path.exists(path):
            dl_mamajek_table(path)  # download the file
        mamajek_df = load_mamajek_from_file(path)
    teff = float(teff)
    teff_unc = float(teff_unc)
    d_mag = float(d_mag)
    dm_unc = float(dm_unc)
    teff_index = ((mamajek_df['Teff'] - teff).abs()).idxmin()
    lower_teff_index = ((mamajek_df['Teff'] - (teff-teff_unc)).abs()).idxmin()
    upper_teff_index = ((mamajek_df['Teff'] - (teff+teff_unc)).abs()).idxmin()

    if filter in ["K", "Ks", "Kcont", "Brgamma"]:
        filter_output = "M_Ks"
    elif filter in ["H", "Hcont"]:
        filter_output = "M_H"
    else:
        filter_output = f"M_{filter}"
        
    if filter_output not in mamajek_df.columns:
        # return f"ERROR: attempted to reference unsupported magnitude '{filter}' - could not run analysis"
        raise ValueError(f"Attempted to reference unsupported filter '{filter}' - could not run analysis")
    
    
    primary_spt = mamajek_df.loc[teff_index, 'SpT']
    primary_spt_lower = mamajek_df.loc[lower_teff_index, 'SpT']
    primary_spt_upper = mamajek_df.loc[upper_teff_index, 'SpT']
    
    primary_mag = mamajek_df.loc[teff_index, filter_output]
    primary_mag_lower = mamajek_df.loc[lower_teff_index, filter_output]
    primary_mag_upper = mamajek_df.loc[upper_teff_index, filter_output]

    # print(type(mamajek_df[filter_output]))
    # print(type(primary_mag))
    # print(type(d_mag))
    comp_index = ((mamajek_df[filter_output] - (primary_mag + d_mag)).abs()).idxmin()
    comp_index_lower = ((mamajek_df[filter_output] - (primary_mag_lower + (d_mag-dm_unc))).abs()).idxmin()
    comp_index_upper = ((mamajek_df[filter_output] - (primary_mag_upper + (d_mag+dm_unc))).abs()).idxmin()

    comp_spt = mamajek_df.loc[comp_index, 'SpT']
    comp_spt_lower = mamajek_df.loc[comp_index_lower, 'SpT']
    comp_spt_upper = mamajek_df.loc[comp_index_upper, 'SpT']

    comp_mag = mamajek_df.loc[comp_index, filter_output]
    comp_mag_lower = mamajek_df.loc[comp_index_lower, filter_output]
    comp_mag_upper = mamajek_df.loc[comp_index_upper, filter_output]
    

    return {
        "primary_spt": primary_spt,
        "primary_spt_lower": primary_spt_lower,
        "primary_spt_upper": primary_spt_upper,
        "comp_spt": comp_spt,
        "comp_spt_lower": comp_spt_lower,
        "comp_spt_upper": comp_spt_upper,
        "primary_mag": primary_mag,
        "primary_mag_lower": primary_mag_lower,
        "primary_mag_upper": primary_mag_upper,
        "comp_mag": comp_mag,
        "comp_mag_lower": comp_mag_lower,
        "comp_mag_upper": comp_mag_upper
        
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("teff", type=float)
    parser.add_argument("teff_unc", type=float)
    parser.add_argument("filter", type=str)
    parser.add_argument("d_mag", type=float)
    parser.add_argument("dm_unc", type=float)
    args = parser.parse_args()
    # mamajek_df = load_mamajek_from_file()
    result = spectral_type(args.teff, args.teff_unc, args.filter, args.d_mag, args.dm_unc)
    print(result)


## To run script: python spectral.py teff_num teff_unc_num filter_name d_mag_num d_mag_unc_num
        ## EX: python spectral.py 6280 122 K 7.031 0.00722
        ## Should return: {'primary_spt': 'F7V', 'comp_spt': 'M7V'}
