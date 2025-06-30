import argparse
from position import position
from magnitude import magnitude
from spectral import spectral_type, load_mamajek_from_file
from dl_mamajek import dl_mamajek
from teff import get_teff, load_exo_df_from_file
from dl_exo import dl_exo
import os
from datetime import datetime
import re

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        tag = s
        print(tag)
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD"
        raise argparse.ArgumentTypeError(msg)

def parse_obs_date_and_data_tag(obs_raw, tag_raw):
    obs_date = None
    data_tag = None

    # If both were passed correctly
    if obs_raw and tag_raw:
        try:
            obs_date = datetime.strptime(obs_raw, "%Y-%m-%d").date()
            data_tag = int(tag_raw)
        except ValueError:
            raise ValueError(f"Invalid obs_date '{obs_raw}'. Expected format YYYY-MM-DD.")
    
    # If only one is provided, try to detect which it is
    elif obs_raw and not tag_raw:
        if obs_raw.isdigit():
            if len(obs_raw) == 8:
                # Looks like YYYYMMDD
                str1, str2, str3 = obs_raw[:4], obs_raw[4:6], obs_raw[6:8]
                try:
                    obs_date = datetime.strptime(f"{str1}-{str2}-{str3}", "%Y-%m-%d").date()
                except ValueError:
                    # Looks like a tag instead
                    data_tag = int(obs_raw)
            else:
                # Too short — assume tag
                data_tag = int(obs_raw)
        else:
            # Try parsing as a normal YYYY-MM-DD string
            try:
                obs_date = datetime.strptime(obs_raw, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Unrecognized value '{obs_raw}'. Must be a date (YYYY-MM-DD) or a numeric tag.")
    # Nothing passed — both remain None

    return obs_date, data_tag


def get_all(id_tag, pixscale, p_x, p_y, c_x, c_y, filter, p_mag, p_unc, c_mag, c_unc, obs_date=None, data_tag=None, exo_df=None, mamajek_df=None):
    # sep, sep_unc, pa, pa_unc = position(p_x, p_y, c_x, c_y)
    # return (sep, sep_unc, pa, pa_unc)
    # if exo_df is None:
    #     print("exo_df is none")
    #     from teff import load_exo_df_from_file
        # exo_df = load_exo_df_from_file()
    # if tag_df is None:
    #     from tag import load_tag_df_from_file
    #     tag_df = load_tag_df_from_file()
    # if mamajek_df is None:
    #     from spectral import load_mamajek_from_file
    #     mamajek_df = load_mamajek_from_file()
    pos_data = position(pixscale, p_x, p_y, c_x, c_y)
    mag_data = magnitude(p_mag, p_unc, c_mag, c_unc)
    temp_data = get_teff(id_tag, exo_df)
    if type(obs_date) == str and len(obs_date) == 10:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", obs_date):
            obs_date = obs_date
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", obs_date):
            return "ERROR: You may have provided a date in MM-DD-YYYY or DD-MM-YYYY format. Please ensure your date is in YYYY-MM-DD format"
    if type(obs_date) == str and len(obs_date) != 10:
        return "ERROR: Please ensure your date is in YYYY-MM-DD format, using hyphens and leading zeroes if necessary—i.e., March is 03"
    if type(obs_date) == int and data_tag is not None:
        return "ERROR: Please ensure your date is provided as a string using YYYY-MM-DD format"
    if type(obs_date) == int and data_tag is None:
        if len(str(obs_date)) < 8:
            print(f"Interpreting {obs_date} as data tag.")
            data_tag = obs_date
            obs_date = None
        elif len(str(obs_date)) == 8:
            string = str(obs_date)
            str1 = string[:4]
            str2 = string[4:6]
            str3 = string[6:8]
            obs_date = f"{str1}-{str2}-{str3}"
    # if type(obs_date) != str:
    #     return "ERROR"
    # tag = get_tag(id_tag, tag_df)
    spt_data = spectral_type(temp_data['teff'], temp_data['unc'], filter, mag_data['d_mag'], mag_data['dm_unc'], mamajek_df)

    
    
    return {
        'target': id_tag,
        'separation': pos_data["separation"], 
        'separation_uncertainty': pos_data["separation_uncertainty"], 
        'position_angle': pos_data["position_angle"], 
        'pa_uncertainty': pos_data["pa_uncertainty"],
        'filter_name': filter,
        'filtercent': '',
        'filterwidth': '',
        'finterunits': '',
        'delta_magnitude': mag_data["d_mag"],
        'd_mag_uncertainty': mag_data["dm_unc"],
        'obsdate': obs_date if isinstance(obs_date, str) else (obs_date.isoformat() if obs_date else None),
        'tag': data_tag,
        'group': f"tfopwg",
        'prop_period': 0,
        'primary_spt': spt_data["primary_spt"],
        'companion_spt': spt_data["comp_spt"],
        'teff': temp_data["teff"],
        'teff_uncertainty': temp_data["unc"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run position, magnitude, and spectral type calculations.")

    parser.add_argument("id_tag", type=int)
    # Position inputs
    parser.add_argument("pixscale", type=float)
    parser.add_argument("p_x", type=float)
    parser.add_argument("p_y", type=float)
    parser.add_argument("c_x", type=float)
    parser.add_argument("c_y", type=float)

    parser.add_argument("filter", type=str)

    # Magnitude inputs
    parser.add_argument("p_mag", type=float)
    parser.add_argument("pm_unc", type=float)
    parser.add_argument("c_mag", type=float)
    parser.add_argument("cm_unc", type=float)
    parser.add_argument("obs_date", nargs="?", default=None)
    parser.add_argument("data_tag", nargs="?", type=int, default=None)
    if not os.path.exists("mamajek.csv"):
        dl_mamajek(save_path="mamajek.csv")
    if not os.path.exists("exofop.csv"):
        dl_exo(save_path="exofop.csv")
        
    parser.add_argument("--mamajek_csv", default="mamajek.csv")
    parser.add_argument("--exo_csv", default="exofop.csv")
    args = parser.parse_args()

    mamajek_df = load_mamajek_from_file(args.mamajek_csv)
    exo_df = load_exo_df_from_file(args.exo_csv)

    obs_date, data_tag = parse_obs_date_and_data_tag(args.obs_date, args.data_tag)

    result = get_all(args.id_tag, args.pixscale, args.p_x, args.p_y, args.c_x, args.c_y,
                 args.filter, args.p_mag, args.pm_unc, args.c_mag, args.cm_unc,
                 obs_date, data_tag, exo_df, mamajek_df)

    print(result)
    
