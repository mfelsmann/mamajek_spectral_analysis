import argparse
from position import position
from magnitude import magnitude
from spectral import spectral_type, load_mamajek_from_file
from dl_mamajek import dl_mamajek_table
from teff import get_teff, load_exo_df_from_file
from dl_exo import dl_exofop
import os

def all_file(id_tag, pixscale, p_x, p_y, c_x, c_y, filter, p_mag, p_unc, c_mag, c_unc, xflip, dl_exo, dl_mamajek, exo_df=None, mamajek_df=None):
    dl_exo = dl_exo.strip('"')
    dl_mamajek = dl_mamajek.strip('"')
 
    
    if dl_exo == "yes":
        dl_exofop('exofop.csv')
    elif dl_exo in ["", "no"]:
        exo_df = load_exo_df_from_file()
    else:
        raise ValueError(f"Invalid download flag '{dl_exo}' - expected 'yes', 'no', or ''")

    if exo_df is None:
        exo_df = load_exo_df_from_file()

    if dl_mamajek == "yes":
        dl_mamajek_table('mamajek.csv')
    elif dl_mamajek in ["", "no"]:
        mamajek_df = load_mamajek_from_file()
    else:
        raise ValueError(f"Invalid download flag '{dl_mamajek}' - expected 'yes', 'no', or ''")
    
    if mamajek_df is None:
        mamajek_df = load_mamajek_from_file()

    if filter in ["K", "Ks", "Kcont", "Brgamma"]:
        filter_output = "M_Ks"
    elif filter in ["H", "Hcont"]:
        filter_output = "M_H"
    else:
        filter_output = f"M_{filter}"

    if filter_output not in mamajek_df.columns:
        raise ValueError(f"Attempted to reference unsupported filter '{filter}' - could not run analysis")
        
    pos_data = position(pixscale, p_x, p_y, c_x, c_y, xflip)
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
        'd_mag': mag_data["d_mag"],
        'd_mag_unc': mag_data["dm_unc"],
        'p_spt': spt_data["primary_spt"],
        'c_spt': spt_data["comp_spt"]
    }

def mamajek_table_lookupfile(input_file, output_file, mamajek_df=None, exo_df=None):
    if mamajek_df is None:
        from spectral import load_mamajek_from_file
        mamajek_df = load_mamajek_from_file()
    if exo_df is None:
        from teff import load_exo_df_from_file
        exo_df = load_exo_df_from_file()
   
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        headers = [
            "target",
            "separation",
            "separation_uncertainty",
            "position_angle",
            "pa_uncertainty",
            "filter_name",
            "delta_magnitude",
            "dm_uncertainty",
            "primary_spt",
            "companion_spt"
        ]
        outfile.write('|'.join(headers) + '\n')
        for line_number, line in enumerate(infile, start=1):
            parts = line.strip().split(',')
            param_count = len(parts)
            if param_count != 14:
                id_tag = parts[0]
                error_msg = (
                    f"{id_tag}|ERROR on line {line_number}: Incorrect number of parameters"
                )
                outfile.write(error_msg + '\n')
                continue

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
                xflip = parts[11]
                dl_exo = parts[12]
                dl_mamajek = parts[13]

                result = all_file(id_tag, pixscale, p_x, p_y, c_x, c_y, filter,
                             p_mag, p_unc, c_mag, c_unc, xflip, dl_exo, dl_mamajek,
                             exo_df=exo_df, mamajek_df=mamajek_df)

                result['p_spt'] = f"{result['p_spt']}"
                result['c_spt'] = f"{result['c_spt']}"

                output_line = '|'.join(str(result.get(key, '')) for key in [
                    'target', 'sep', 'sep_unc', 'pa', 'pa_unc', 'filter_name',
                    'd_mag', 'd_mag_unc', 'p_spt', 'c_spt'
                ])
            except Exception as e:
                output_line = f"ERROR on line {line_number}: {e}"

            outfile.write(output_line + '\n')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run position, magnitude, and spectral type calculations.")
    parser.add_argument("input_file", help="Path to input file with parameters")
    parser.add_argument("output_file", help="Path to output file to save results")

    args = parser.parse_args()

    if not os.path.exists("mamajek.csv"):
        dl_mamajek(save_path="mamajek.csv")
    if not os.path.exists("exofop.csv"):
        dl_exo(save_path="exofop.csv")



    mamajek_df = load_mamajek_from_file()
    exo_df = load_exo_df_from_file()

    mamajek_table_lookupfile(args.input_file, args.output_file, mamajek_df, exo_df)

