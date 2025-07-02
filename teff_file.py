import numpy as np
import pandas as pd
import argparse
from dl_exo import dl_exo
import os

def load_exo_df_from_file(path='exofop.csv'):
    return pd.read_csv(path)

def get_teff_file(id_tag, exo_df=None, path='exofop.csv'):
    if exo_df is None:
        if not os.path.exists(path):
            dl_exo(path)  # download the file
        exo_df = load_exo_df_from_file(path)
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
            
    index_value = index[0]
    teff = exo_df.loc[index_value, 'Stellar Eff Temp (K)']
    teff_unc_raw = exo_df.loc[index_value, 'Stellar Eff Temp (K) err']
    teff_unc = teff_unc_raw if pd.notna(teff_unc_raw) and teff_unc_raw != '' else 0

    return {"teff": teff, 
            "teff_unc": teff_unc
           }

def teff_file(input_file, output_file, exo_df=None, path='exofop.csv'):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        headers = [
            "effective_temperature",
            "teff_uncertainty"
        ]
        outfile.write('|'.join(headers) + '\n')
        for line_number, line in enumerate(infile, start=1):
            try: 
                tag = float(line.strip())
                result = get_teff_file(tag, exo_df)
                output_line = '|'.join(str(result.get(key, '')) for key in [
                    'teff',
                    'teff_unc',
                ])
            except Exception as e:
                output_line = f"ERROR on line {line_number}: {e}"

            outfile.write(output_line + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file with parameters")
    parser.add_argument("output_file", help="Path to input file with parameters")
    args = parser.parse_args()
    if not os.path.exists("exofop.csv"):
        dl_exo(save_path="exofop.csv")
    exo_df = load_exo_df_from_file()
    teff_file(args.input_file, args.output_file, exo_df)

## To run script: python teff_file.py input_file_name.txt output_file_name.txt
    ## EX: python teff_file.py test_tags.txt test_tags_output.txt
        ## Where test_tags.txt has content: 7011
        ##                                  3588
    ## Should create file with content: 5493.0|140.6
    ##                                  6688.0|137.9