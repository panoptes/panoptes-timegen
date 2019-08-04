# The command line script that generates the timelapse
# Libraries imported here.
import logging
import click
import os
import sys
import numpy as np
import astropy.io.fits as fits

# Configure log file
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='..\logs.log',
                filemode='w',
                level=logging.INFO)

#Step 0: Read command line args
@click.command()
@click.option('--in_path','-i',help='Path to the directory containing the FITS files.',required=True)
@click.option('--out_path','-o',help='Location at where the timelapse will be saved.')
@click.option('--options',help='Additional options to be specified.')
def main(in_path,out_path,options):
    """ Generates a timelapse from the input FITS files (directory) and saves it to the given path.
        ----------
        parameters
        ----------
        in_path  : The path to the directory containing the input FITS files (*.fits or *.fits.fz)
        out_path : The path at which the output timelapse will be saved. If unspecified writes to .\timelapse
        options  : Additional options.   
        ----------
        returns
        ----------
        True if timelapse generated successfully.
    """
    fits_files = get_file_list(in_path)
    #TO DO

def get_file_list(path):
    """ Helper function to validate the given in_path. Checks if the path is valid and if valid checks if the 
        directory contains valid FITS files. (*.fits or *.fits.fz)
        ----------
        parameters
        ----------
        path : The path from which to retrieve the FITS files.
        ----------
        returns
        ----------
        List of filenames if path is valid.
    """
    if not os.path.isdir(path):
        logging.error('Directory invalid')
        sys.exit('Directory invalid')
    else:
        fits_list = []
        # The FITS files are named in numerically ascending order with an optional 
        for file in os.listdir(path):
            if file.endswith('fits.fz') or file.endswith('.fits'):
                fits_list.append(os.path.join(path,file))
        if len(fits_list) == 0:
            logging.error('No FITS files found')   
            sys.exit("No FITS files found in the directory")        
    return sorted(fits_list)        
       
        
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