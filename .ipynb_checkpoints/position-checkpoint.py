import argparse
import numpy as np

def position(pixscale, p_x, p_y, c_x, c_y):
	sep_delta_x = abs(p_x - c_x)
	sep_delta_y = abs(p_y - c_y)
	pos_error = np.sqrt(2)*0.1*pixscale
	
	separation = np.sqrt(sep_delta_x**2 + sep_delta_y**2)*pixscale
	separation_round = round(separation, 3)
	sep_unc = np.sqrt(4*((sep_delta_y*pos_error)**2 + (sep_delta_x*pos_error)**2))*pixscale
	sep_unc_round = round(sep_unc, 3)
	pa_delta_x = c_x - p_x
	pa_delta_y = c_y - p_y
	pa_theta = np.arctan2(pa_delta_x, pa_delta_y)
	pa = (np.degrees(pa_theta)) % 360
	pa_round = round(pa, 3)
	pa_unc = np.degrees(np.sqrt(((0.003592102448*sep_delta_x)/(separation**2))**2 + ((0.003592102448*sep_delta_y)/(separation**2))**2))*pixscale
	pa_unc_round = round(pa_unc, 3)

	return { "separation": separation_round, 
            "separation_uncertainty": sep_unc_round, 
            "position_angle": pa_round, 
            "pa_uncertainty": pa_unc_round
           }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", required=True, type=float, help="Pixel scale")
    parser.add_argument("p_x", type=float, help="Centroid X coordinate of the primary star")
    parser.add_argument("p_y", type=float, help="Centroid Y coordinate of the primary star")
    parser.add_argument("c_x", type=float, help="Centroid X coordinate of the companion star")
    parser.add_argument("c_y", type=float, help="Centroid Y coordinate of the companion star")
    args = parser.parse_args()

    result = position(args.s, args.p_x, args.p_y, args.c_x, args.c_y)
    print(result)


## To run script: python position.py --s pixscale p_x p_y c_x c_y
    ## EX: python position.py --s 0.0254 100 200 150 250 
    ## Should return: {'separation': 1.796, 'separation_uncertainty': 0.013, 'position_angle': 45.0, 'pa_uncertainty': 0.115}
    ## NB: pixel scale can be anywhere in list of inputs: --s pixscale p_x p_y c_x c_y OR p_x p_y c_x c_y --s pixscale OR p_x p_y --s pixscale c_x c_y are all valid