import pandas as pd
import numpy as np
import argparse
from dl_mamajek import dl_mamajek
import os

def load_mamajek_from_file(path='mamajek.csv'):
    return pd.read_csv(path)

def spectral_type_file(teff, teff_unc, filter, d_mag, dm_unc, mamajek_df=None, path='mamajek.csv'):
    if mamajek_df is None:
        if not os.path.exists(path):
            dl_mamajek(path)  # download the file
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
        raise ValueError(f"Attempted to reference unsupported magnitude '{filter}' - could not run analysis - spectral file")
    
    
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
        "primary_mag": primary_mag,
        "primary_mag_lower": primary_mag_lower,
        "primary_mag_upper": primary_mag_upper,
        "comp_spt": comp_spt,
        "comp_spt_lower": comp_spt_lower,
        "comp_spt_upper": comp_spt_upper,
        "comp_mag": comp_mag,
        "comp_mag_lower": comp_mag_lower,
        "comp_mag_upper": comp_mag_upper
        
    }

def spectral_file(input_file, output_file, mamajek_df=None, path='mamajek.csv'):
    if mamajek_df is None:
        if not os.path.exists(path):
            dl_mamajek(path)  # download the file
        mamajek_df = load_mamajek_from_file(path)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_number, line in enumerate(infile, start=1):
            parts = line.strip().split(',')
            
            try:
                teff = parts[0]
                teff_unc = parts[1]
                filter = parts[2]
                d_mag = parts[3]
                dm_unc = parts[4]
            # print(teff, teff_unc, filter, d_mag, dm_unc)
                result = spectral_type_file(
                    float(teff),
                    float(teff_unc),
                    filter,
                    float(d_mag),
                    float(dm_unc),
                    mamajek_df
                )
                output_line = '|'.join(str(result.get(key, '')) for key in [
                    "primary_spt",
                    "primary_spt_lower",
                    "primary_spt_upper",
                    "primary_mag",
                    "primary_mag_lower",
                    "primary_mag_upper",
                    "comp_spt",
                    "comp_spt_lower",
                    "comp_spt_upper",
                    "comp_mag",
                    "comp_mag_lower",
                    "comp_mag_upper"
                ])
            except Exception as e:
                # Write the error message in the output line and continue
                output_line = f"ERROR on line {line_number}: {e}"

            outfile.write(output_line + '\n')



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file with parameters")
    parser.add_argument("output_file", help="Path to output file to save results")
    args = parser.parse_args()
    # if not os.path.exists("mamajek.csv"):
    #     dl_mamajek(save_path="mamajek.csv")
    #     # print('Downloaded and saved mamajek.csv to cwd')
    # mamajek_df = load_mamajek_from_file()

    spectral_file(args.input_file, args.output_file)

