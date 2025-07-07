import argparse
from position import position
from magnitude import magnitude
from spectral import spectral_type, load_mamajek_from_file
from dl_mamajek import dl_mamajek_table
from teff import get_teff, load_exo_df_from_file
from dl_exo import dl_exofop
import os
import re


def mamajek_table_lookup(id_tag, pixscale, p_x, p_y, c_x, c_y, filter, p_mag, p_unc, c_mag, c_unc, xflip, dl_exo="no", dl_mamajek="no", exo_df=None, mamajek_df=None):
    
    if exo_df is None:
        if dl_exo == "yes":
            dl_exofop('exofop.csv')
            exo_df = load_exo_df_from_file()
        elif dl_exo in ["", "no"]:
            exo_df = load_exo_df_from_file()
    if mamajek_df is None:
        if dl_mamajek == "yes":
            dl_mamajek_table('mamajek.csv')
            mamajek_df = load_mamajek_from_file()
        elif dl_mamajek in ["", "no"]:
            mamajek_df = load_mamajek_from_file()
        
        
    if filter in ["K", "Ks", "Kcont", "Brgamma"]:
        filter_output = "M_Ks"
    elif filter in ["H", "Hcont"]:
        filter_output = "M_H"
    else:
        filter_output = f"M_{filter}"

        
    pos_data = position(pixscale, xflip, p_x, p_y, c_x, c_y)
    mag_data = magnitude(p_mag, p_unc, c_mag, c_unc)
    temp_data = get_teff(id_tag, exo_df)
  
    spt_data = spectral_type(temp_data['teff'], temp_data['unc'], filter, mag_data['d_mag'], mag_data['dm_unc'], mamajek_df)

    
    
    return {
        'target': id_tag,
        'separation': pos_data["separation"], 
        'separation_uncertainty': pos_data["separation_uncertainty"], 
        'position_angle': pos_data["position_angle"], 
        'pa_uncertainty': pos_data["pa_uncertainty"],
        'filter_name': filter,
        # 'filtercent': '',
        # 'filterwidth': '',
        # 'finterunits': '',
        'delta_magnitude': mag_data["d_mag"],
        'd_mag_uncertainty': mag_data["dm_unc"],
        # 'group': f"tfopwg",
        # 'prop_period': 0,
        'primary_spt': spt_data["primary_spt"],
        'companion_spt': spt_data["comp_spt"],
        # 'teff': temp_data["teff"],
        # 'teff_uncertainty': temp_data["unc"],
        # 'obsdate': obs_date if isinstance(obs_date, str) else (obs_date.isoformat() if obs_date else None),
        # 'tag': data_tag,
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
    parser.add_argument("xflip", type=str)
    parser.add_argument("--dl_exo", choices=["yes", "no", ""], default="no", help="Whether to re-download the ExoFOP CSV.")
    parser.add_argument("--dl_mamajek", choices=["yes", "no", ""], default="no", help="Whether to re-download the Mamajek CSV.")
    
    
        
    parser.add_argument("--mamajek_csv", default="mamajek.csv")
    parser.add_argument("--exo_csv", default="exofop.csv")
    args = parser.parse_args()
    if not os.path.exists("mamajek.csv") or args.dl_mamajek == "yes":
        dl_mamajek_table(save_path="mamajek.csv")
    if not os.path.exists("exofop.csv") or args.dl_exo == "yes":
        dl_exofop(save_path="exofop.csv")
        

    mamajek_df = load_mamajek_from_file(args.mamajek_csv)
    exo_df = load_exo_df_from_file(args.exo_csv)

    # obs_date, data_tag = parse_obs_date_and_data_tag(args.obs_date, args.data_tag)

    result = mamajek_table_lookup(args.id_tag, args.pixscale, args.p_x, args.p_y, args.c_x, args.c_y,
                 args.filter, args.p_mag, args.pm_unc, args.c_mag, args.cm_unc, args.xflip, args.dl_exo, args.dl_mamajek, exo_df, mamajek_df)

    print(result)
    
