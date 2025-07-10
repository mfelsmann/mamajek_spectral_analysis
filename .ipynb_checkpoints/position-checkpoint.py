import argparse
import numpy as np
import sys


class ArgumentParser(argparse.ArgumentParser): # Creates subclass of argparse.ArgumentParser
    def error(self, message): # Define function "error" with two input parameters
        self.exit(2, 'ERROR: %s\n' % (message)) # Exit and print message (2 = CL syntax error)

def position(pixscale, p_x, p_y, c_x, c_y, xflip):
    if xflip == "xflip":
        multiplier = -1
    elif xflip == "noxflip":
        multiplier = 1
    sep_delta_x = abs(p_x - c_x)
    sep_delta_y = abs(p_y - c_y)
    pos_error = np.sqrt(2)*0.1*pixscale

    separation = np.sqrt(sep_delta_x**2 + sep_delta_y**2)*pixscale
    separation_round = round(separation, 3)
    sep_unc_round = round((np.sqrt(4*((sep_delta_y*pos_error)**2 + (sep_delta_x*pos_error)**2))*pixscale), 3)
    pa_delta_x = (c_x - p_x)*(-1)*multiplier
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
    parser = ArgumentParser()
    parser.add_argument("--s", required=True, type=float, help="Instrument pixel scale")
    parser.add_argument("p_x", type=float, help="Centroid X coordinate of the primary star")
    parser.add_argument("p_y", type=float, help="Centroid Y coordinate of the primary star")
    parser.add_argument("c_x", type=float, help="Centroid X coordinate of the companion star")
    parser.add_argument("c_y", type=float, help="Centroid Y coordinate of the companion star")
    parser.add_argument("--f", required=True, type=str, help="Reflect X coordinates to correct for coordinate system orientation")
    args = parser.parse_args()
    result = position(args.s, args.p_x, args.p_y, args.c_x, args.c_y, args.f)
    print(result)

## Notebook: position(pixscale, p_x, p_y, c_x, c_y, "xflip")
## CLI: python position.py --s pixscale p_x p_y c_x c_y --f xflip
    ## NB: pixel scale can be anywhere in list of inputs: --s pixscale p_x p_y c_x c_y OR p_x p_y c_x c_y --s pixscale OR p_x p_y --s pixscale c_x c_y are all valid
## xflip options: "xflip" or "noxflip"
