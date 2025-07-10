import argparse
import numpy as np

class ArgumentParser(argparse.ArgumentParser): # Creates subclass of argparse.ArgumentParser
    def error(self, message):
        if "required:" in message:
            self.exit(2, "ERROR: Too few arguments provided. Expected 4 values: p_mag, pm_unc, c_mag, cm_unc\n")
        elif "unrecognized arguments:" in message:
            self.exit(2, "ERROR: Too many arguments provided or unrecognized input.\n")
        else:
            self.exit(2, f"ERROR: {message}\n")


def magnitude(p_mag, pm_unc, c_mag, cm_unc):
    d_mag = c_mag - p_mag
    dm_round = round(d_mag, 3)
    dm_unc = np.sqrt((pm_unc**2) + (cm_unc**2))
    dm_unc_round = round(dm_unc, 3)

    return {
        "dmag": d_mag,
        "d_mag": dm_round,
        "dm_unc": dm_unc_round
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("p_mag", type=float, help="Primary star magnitude")
    parser.add_argument("pm_unc", type=float, help="Primary star magnitude uncertainty")
    parser.add_argument("c_mag", type=float, help="Companion star magnitude")
    parser.add_argument("cm_unc", type=float, help="Companion star magnitude uncertainty")
    args = parser.parse_args()

    result = magnitude(args.p_mag, args.pm_unc, args.c_mag, args.cm_unc)
    print(result)

## Notebook: magnitude(p_mag, pm_unc, c_mag, cm_unc)
## CLI: python magnitude.py p_mag pm_unc c_mag cm_unc