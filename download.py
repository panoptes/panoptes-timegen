import os
import click
import tqdm
import urllib.request

def file_download(url,fname):
    """
    url: The url to the panoptes cloud storage from where to retrieve the FITS file
    filename: The name with which to save the file.
    path_to_dir: The path to the folder where the file has to be saved
    -------------------------------------------------------------------------------
    returns: True if successful.
    
    """
    try:
        urllib.request.urlretrieve(url,fname)
    except Exception as e:
        print(e)
    return True



 
@click.command()
@click.option('-i','--in_file',type=click.File('r'),help="Text file with URLs of FITS images",required=True)
@click.option('-o','--out',type=str,help='Path to output directory',default = r'.')
def downloader(in_file,out):
    """Downloads and stores the FITS files to a directory from a text file downloaded from panoptes-data.net \n
    ----------- \n
    parameters  \n
    ----------- \n
    in_file: The input text file containing the URLs of the FITS files \n
    out: The directory to write the files to. Defaults to current directory. \n
    ----------- \n
    returns \n  
    ----------- \n
    True if all files are successfully written 
    """
    url_list = in_file.readlines()
    print('File contains {0} urls'.format(len(url_list)))
    for url in tqdm.tqdm(url_list):
        # Get path to file directory
        path_to_dir = os.path.join(out,url.split('/')[-2])
        if not os.path.isdir(path_to_dir):
            os.makedirs(path_to_dir,exist_ok = True)
            
        #Creates directory if doesn't exist    
        filename = url.split('/')[-1].strip()
        
        #Get filename from url
        fname = os.path.join(path_to_dir,filename)
        
        #Don't download if already exists
        if os.path.isfile(fname):
            print("The file {0} already exists".format(filename))
        else:
            file_download(url,fname)
    return True        

if __name__ == '__main__':
    downloader()