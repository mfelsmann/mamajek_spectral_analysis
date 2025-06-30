import numpy as np
import pandas as pd
from astropy.io import ascii
import requests

def dl_exo(save_path='exofop.csv'):
    exo_url = 'https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv'
    exofop_response = requests.get(exo_url)
    lines = exofop_response.text.splitlines()
    exo_data_table = ascii.read(lines, format='basic', delimiter=',', fill_values=[('null', np.nan)])
    exo_df = exo_data_table.to_pandas()
    exo_df.to_csv(save_path, index=False)

if __name__ == "__main__":
    dl_exo()


## To run script: python dl_exo.py