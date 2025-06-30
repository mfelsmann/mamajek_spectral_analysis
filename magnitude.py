import argparse
import numpy as np

def magnitude(p_mag, pm_unc, c_mag, cm_unc): 
    d_mag = c_mag - p_mag
    dm_round = round(d_mag, 3)
    dm_unc = np.sqrt((pm_unc**2) + (cm_unc**2))
    dm_unc_round = round(dm_unc, 3)

    return {
        "d_mag": dm_round,
        "dm_unc": dm_unc_round
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("p_mag", type=float)
    parser.add_argument("pm_unc", type=float)
    parser.add_argument("c_mag", type=float)
    parser.add_argument("cm_unc", type=float)
    args = parser.parse_args()

    result = magnitude(args.p_mag, args.pm_unc, args.c_mag, args.cm_unc)
    print(result)

## To run script: python magnitude.py p_mag pm_unc c_mag cm_unc
    ## EX: python magnitude.py 11.8986 0.00291312 16.3363 0.0213935
    ## Should return: {'d_mag': 4.438, 'dm_uncertainty': 0.022}