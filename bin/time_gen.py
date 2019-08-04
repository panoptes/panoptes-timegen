# The command line script that generates the timelapse
# Libraries imported here.
import click
import os
import tqdm
import numpy as np
import astropy.io.fits as fits

#Step 0: Read command line args
@click.command()
@click.option('--in_path','-i',help='Path to the directory containing the FITS files.',required=True)
@click.option('--out_path','-o',help='Location at where the timelapse will be saved.')
@click.option('--options',help='Additional options to be specified.')
def main(in_path,out_path,options):
    """ Generates a timelapse from the input FITS files (directory) and saves it to the given path."""
    print(in_path,out_path)

# A broad overview of the pipeline
# 1. Get directory of FITS files. One directory of observations. If download txt file specified, take care of everything.

# 2. For each FITS file:
#   a. debayer and get R,G,B arrays of type np.uint16
#   b. <contrast stretching> <histogram equalization>
#   c. generate final image. 'jpg' preferably. 
#   d. store jpg to temporary location.

# 3. Take files from temporary location and build timelapse from them.

# Other Requirements: Should be able to continue from where it left off in case of breakdown.    

#Step 1:
# Check if the given directory is valid. If not valid: exit and show proper usage guidelines
# If directory is valid, display summary of folder contents and proceed to .
if __name__ == '__main__':
    main()