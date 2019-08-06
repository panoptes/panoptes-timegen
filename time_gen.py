# The command line script that generates the timelapse
# Libraries imported here.
import logging
import click
import os
import sys
import numpy as np
import astropy.io.fits as fits
from colour_demosaicing import demosaicing_CFA_Bayer_bilinear, demosaicing_CFA_Bayer_Malvar2004 , demosaicing_CFA_Bayer_Menon2007

# Configure log file
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='..\logs.log',
                filemode='w',
                level=logging.INFO)

logging.info('Importing finished')                
# logging errors and exiting
def log_error_exit(message):
    """ Simple wrappper around the logging.error and sys.exit functions. Logs the ERROR message to the log file
        and exits the program with the same message sent to stdout.
    """
    logging.error(message)
    sys.exit(message)

#Step 0: Read command line args
def get_file_list(path):
    """ Helper function to validate the given in_path. Checks if the path is valid and if valid checks if the 
        directory contains valid FITS files and returns a list of paths. (*.fits or *.fits.fz)
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
        log_error_exit('Directory invalid.')
    else:
        fits_list = []
        # The FITS files are named in numerically ascending order with an optional 
        for file in os.listdir(path):
            if file.endswith('fits.fz') or file.endswith('.fits'):
                fits_list.append(os.path.join(path,file))
        if len(fits_list) == 0:
            log_error_exit('No FITS files found !')       
    return sorted(fits_list)        
       
def debayer_image_array(data, algorithm = 'bilinear',pattern = 'GRGB'):
    """ Returns the RGB data after bilinear interpolation on the given array.
        ----------
        parameters  
        ----------
        data : The input array containing the image data. Array like of shape (rows,columns)
        algorithm : The algorithm to use for the debayering operation. 
        {'bilinear','malvar2004','menon2007'}
        ----------
        returns
        ----------
        numpy array of shape (rows,columns,3)
    """
    # Check to see if data is two dimensional
    try:
        assert len(data.shape) == 2, 'Shape is not 2 dimensional'
    except AssertionError:    
        log_error_exit('Image data input to debayer is not 2 dimensional')

    if algorithm == 'bilinear':
        rgb_data = demosaicing_CFA_Bayer_bilinear(data, pattern)
    elif algorithm == 'malvar2004':
        rgb_data = demosaicing_CFA_Bayer_Malvar2004(data, pattern)
    elif algorithm == 'menon2007':
        rgb_data = demosaicing_CFA_Bayer_Menon2007(data,pattern)
    return rgb_data            

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
    
    for fits_file in fits_files:
        fits_data = fits.getdata(fits_file)
        rgb_data = debayer_image_array()
        rgb_image = Image(rgb_data)
        status = rgb_image.writeto()#TEMP)
        


if __name__ == '__main__':
    main()