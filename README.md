# A Python Program for Spectral Type Analysis

This program is a complementary tool to Eric Mamajek's "[A Modern Mean Dwarf Stellar Color and Effective Temperature Sequence](https://github.com/emamajek/SpectralType/blob/master/EEM_dwarf_UBVIJHK_colors_Teff.txt)" table. Given a few basic parameters such as target ID and magnitude, this program will produce an overview of the spectral types of a primary and companion star set.

## Repository Content

- `download_flags_walkthrough.ipynb` - explains how to use the optional database download parameters in function calls
- `notebook_full_walkthrough.ipynb` - complete explanation of all features of program
- `combined_example_description.md` - description of each line of input parameters in `combined_example.txt`
- `combined_example_output.txt` - the output file created by running `mamajek_table_lookupfile.py` on `combined_example.txt`
- `combined_example.txt` - example input file for running `mamajek_table_lookupfile.py`
- `dl_exo.py` - Python file for downloading and saving the ExoFOP database
- `dl_mamajek.py` - Python file for downloading and saving Eric Mamajek's spectral type table
- `exofop.csv` - pre-loaded ExoFOP database—re-download as needed
- `magnitude.py` - Python file for calculating magnitude difference between a primary and companion star
- `mamajek_table_lookup.py` - Python file for running full stellar analysis on a primary-companion pair—intended for use on a single set
- `mamajek_table_lookupfile.py` - Python file for running full stellar analysis on primary-companion pairs—intended for use on a file of multiple sets
- `mamajek.csv` - pre-loaded Mamajek table—re-download as needed
- `position.py` - Python file for calculating separation and position angle between a primary and companion star
- `README.md` - this file
- `spectral_example_output.txt` - the output file created by running `spectral_file.py` on `spectral_example.txt`
- `spectral_example.txt` - example input file for running `spectral_file.py`
- `spectral_file.py` - Python file for calculating the respective spectral types of primary-companion pairs—intended for use on a file of multiple sets
- `spectral.py` - Python file for calculating the respective spectral types of a primary-companion pair—intended for use on a single set
- `teff_example_output.txt` - the output file created by running `teff_file.py` on `teff_example.txt`
- `teff_example.txt` - example input file for running `teff_file.py`
- `teff_file.py` - Python file for retrieving the effective temperature of a primary star—intended for use on a file of multiple stars
- `teff.py` - Python file for retrieving the effective temperature of a primary star—intended for use on a single star

## Recent Changes

- `teff.py` and `teff_file.py` edited to support greater range of TIC candidates by pulling from MAST catalog using `astroquery`
- `combined_example_description` changed from `.txt` to `.md` file format