import argparse
from position import position
from magnitude import magnitude
from spectral import spectral_type, load_mamajek_from_file
from dl_mamajek import dl_mamajek
from teff import get_teff, load_exo_df_from_file
from dl_exo import dl_exo
import os
import re
from datetime import datetime

def valid_date_file(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD"
        raise argparse.ArgumentTypeError(msg)

def all(id_tag, pixscale, p_x, p_y, c_x, c_y, filter, p_mag, p_unc, c_mag, c_unc, obs_date, data_tag, exo_df=None, mamajek_df=None):
    obs_date = obs_date.strip()
    if obs_date:
        # Enforce strict YYYY-MM-DD format using regex
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", obs_date):
            raise ValueError(f"Invalid date format for observation date '{obs_date}'. Expected format: YYYY-MM-DD")

        # Then validate it is a real calendar date
        try:
            datetime.strptime(obs_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid calendar date: '{obs_date}'")

    # sep, sep_unc, pa, pa_unc = position(p_x, p_y, c_x, c_y)
    # return (sep, sep_unc, pa, pa_unc)
    if exo_df is None:
        from teff import load_exo_df_from_file
        exo_df = load_exo_df_from_file()
    if mamajek_df is None:
        from spectral import load_mamajek_from_file
        mamajek_df = load_mamajek_from_file()
    pos_data = position(pixscale, p_x, p_y, c_x, c_y)
    mag_data = magnitude(p_mag, p_unc, c_mag, c_unc)
    temp_data = get_teff(id_tag, exo_df)
    spt_data = spectral_type(temp_data['teff'], temp_data['unc'], filter, mag_data['d_mag'], mag_data['dm_unc'], mamajek_df)
    
    return {
        'target': id_tag,
        'sep': pos_data["separation"], 
        'sep_unc': pos_data["separation_uncertainty"], 
        'pa': pos_data["position_angle"], 
        'pa_unc': pos_data["pa_uncertainty"],
        'filter_name': filter,
        'filtercent': '',
        'filterwidth': '',
        'finterunits': '',
        'd_mag': mag_data["d_mag"],
        'd_mag_unc': mag_data["dm_unc"],
        'obsdate': obs_date,
        'tag': data_tag,
        'group': f"tfopwg",
        'prop_period': 0,
        'p_spt': spt_data["primary_spt"],
        'c_spt': spt_data["comp_spt"]
    }

def all_file(input_file, output_file, mamajek_df=None, exo_df=None, tag_df=None):
    if mamajek_df is None:
        from spectral import load_mamajek_from_file
        mamajek_df = load_mamajek_from_file()
    if exo_df is None:
        from teff import load_exo_df_from_file
        exo_df = load_exo_df_from_file()
   
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_number, line in enumerate(infile, start=1):
            parts = line.strip().split(',')

            try:
                id_tag = parts[0]
                pixscale = float(parts[1])
                p_x = float(parts[2])
                p_y = float(parts[3])
                c_x = float(parts[4])
                c_y = float(parts[5])
                filter = parts[6]
                p_mag = float(parts[7])
                p_unc = float(parts[8])
                c_mag = float(parts[9])
                c_unc = float(parts[10])
                obs_date = parts[11]
                data_tag = parts[12]

                result = all(id_tag, pixscale, p_x, p_y, c_x, c_y, filter,
                             p_mag, p_unc, c_mag, c_unc, obs_date, data_tag,
                             exo_df=exo_df, mamajek_df=mamajek_df)

                result['notes'] = f"Primary spectral type: {result['p_spt']}; companion spectral type: {result['c_spt']}"

                output_line = '|'.join(str(result.get(key, '')) for key in [
                    'target', 'sep', 'sep_unc', 'pa', 'pa_unc',
                    'filter_name', 'filtercent', 'filterwidth', 'filterunits',
                    'd_mag', 'd_mag_unc', 'obsdate', 'tag', 'group',
                    'prop_period', 'notes'
                ])
            except Exception as e:
                output_line = f"ERROR on line {line_number}: {e}"

            outfile.write(output_line + '\n')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run position, magnitude, and spectral type calculations.")
    parser.add_argument("input_file", help="Path to input file with parameters")
    parser.add_argument("output_file", help="Path to output file to save results")

    parser.add_argument("args", nargs='*', help="Manual input mode: id_tag pixscale p_x p_y c_x c_y filter p_mag pm_unc c_mag cm_unc")

    args = parser.parse_args()

    if not os.path.exists("mamajek.csv"):
        dl_mamajek(save_path="mamajek.csv")
    if not os.path.exists("exofop.csv"):
        dl_exo(save_path="exofop.csv")



    mamajek_df = load_mamajek_from_file()
    exo_df = load_exo_df_from_file()

    all_file(args.input_file, args.output_file, mamajek_df, exo_df)

