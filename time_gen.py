# The command line script that generates the timelapse
# Libraries imported here.
import logging
import click
import os
import sys
import numpy as np
import astropy.io.fits as fits
from colour_demosaicing import demosaicing_CFA_Bayer_bilinear, demosaicing_CFA_Bayer_Malvar2004 , demosaicing_CFA_Bayer_Menon2007
import cv2
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
def get_file_list(path , extensions):
    """ Helper function to validate the given in_path. Checks if the path is valid and if valid 
        checks if the directory contains files with the specified extension and returns a list of paths. (*.fits or *.fits.fz)
        ----------
        parameters
        ----------
        path : The path from which to retrieve the files ending in the specified extensions.
        extensions: A list of strings specifiying the extensions to look for. ['jpg','tif']
        ----------
        returns
        ----------
        List of filenames if path is valid.
    """
    if not os.path.isdir(path):
        log_error_exit('Directory invalid.')
    else:
        files_list = []
        # The FITS files are named in numerically ascending order with an optional 
        for file in os.listdir(path):
            if file.split('.')[-1] in extensions:
                files_list.append(os.path.join(path,file))
        if len(files_list) == 0:
            log_error_exit('No files with given extensins found !')       
    return sorted(files_list)        
       
def debayer_image_array(data, algorithm = 'bilinear',pattern = 'GRBG'):
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
    return rgb_data.astype(np.uint16)            

def get_sub_image(data,M,N,m,n):
    """Divides the image into M*N parts and returns the grid on row m and column n
       -----------
       parameters
       -----------
       data -> The image array that we are extracting the sub-image/grid-cell from.
       M -> Number of grid rows
       N -> Number of grid columns
       m -> row index of grid cell we need to return
       n -> column index of grid cell we need to return
       -----------
       returns
       -----------
       Sub array from input array.
    """
    rows,columns = data.shape[0:2]
    assert M<=rows and N<=columns,"Grid dimensions exceed Image dimensions"
    return data[m*int(rows/M) : (m+1)*int(rows/M), n*int(columns/N) : (n+1)*int(columns/N)]
# A broad overview of the pipeline
# 1. Get directory of FITS files. One directory of observations. If download txt file specified, take care of everything.

# 2. For each FITS file:
#   a. debayer and get R,G,B arrays of type np.uint16
#   b. <contrast stretching> <histogram equalization>
#   c. generate final image. 'jpg' preferably. 
#   d. store jpg to temporary location.

# 3. Take files from temporary location and build timelapse from them.

# Other Requirements: Should be able to continue from where it left off in case of breakdown.    
def clear_dir(temp_dir):
    if not os.path.isdir(temp_dir):
        return False
    temp_files = os.listdir(temp_dir)
    if not len(temp_files)== 0:
        # If the temporary directory has files,delete them
        for file in temp_files:
            file_path = os.path.join(temp_dir,file)
            os.remove(file_path)
    return True        

def save_image(image_data, image_name):
    """ Save the given image data as a jpg image at the path specified. A helper function to store the intermediate
    jpg images before generating the timelapse from them.
    
    ------------
    parameters
    ------------
    image_data : numpy array of shape (rows,columns,3) returned by debayering. datatype should be np.uint16
    image_name: The name with which to save the image.
    path : The path to where the frames should be saved.
    
    ------------
    returns
    ------------
    True if file write was successful. Else exits with error.
    """
    temp_dir = 'temp_timelapse'

    if not type(image_data) == np.ndarray:
        log_error_exit('Input not of type np.ndarray')
    
    if not os.path.isdir(temp_dir):
        #if not a directory then create the directory
        os.mkdir(temp_dir)
          
    if image_data.dtype == np.uint16:
        image_name = image_name + '.tif'
    else:
        image_name = image_name + '.jpg'
    
    image_path = os.path.join(temp_dir,image_name)   
    print(image_path,image_name)
    return cv2.imwrite(image_path , image_data)    
    

def generate_timelapse_from_images(path_to_images, output_path):
    """ Read the path to the image files and create a video stream. The output is a single video file
        in mp4 format.
    ------------
    parameters
    ------------
    path_to_images : The file path to the previously generated jpgs/tiffs.
    output_path : The path to where to write the video.

    ------------
    returns
    ------------
    True if video write was successful. Else exits with error.
    """    
    file_list = get_file_list(path_to_images,['jpg','tif'])
    if len(file_list) == 0:
        log_error_exit('No frames found to generate video')
     
    frame_list = [file_name for file_name in file_list if file_name.endswith('tif')]
    # If there are no TIF files, search for JPG files
    if len(frame_list) == 0:
        frame_list = [file_name for file_name in file_list if file_name.endswith('jpg')]
    
    # Read first file and get frame size to define the video writer settings
    pilot_frame = cv2.imread(frame_list[0])
    pilot_name = os.path.split(frame_list[0])[-1]
    video_name = pilot_name.split('.')[0]
    # Essentially, the name of the file is kept as the name of the video. The extension is changed.
    logging.info(video_name)
    height, width = pilot_frame.shape[0:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    try:
        video_writer = cv2.VideoWriter(video_name + '.mp4', fourcc, 1, (width ,height), True)
        logging.info(video_writer.getBackendName())
    except Exception as e:
        logging.error(e)
        print('Error with the VideoWriter. Check to see if you have the right codecs.')
        
    for frame_name in frame_list[1:]:
        frame = cv2.imread(frame_name)
        video_writer.write(frame)
    return True    

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
    fits_files = get_file_list(in_path,['.fits','.fz'])
    
      


if __name__ == '__main__':
    main()