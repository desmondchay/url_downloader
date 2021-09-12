from .util import get_current_disk_space, unique_file, check_file_size, convert_size
from contextlib import closing
import urllib.request as ftprequest, urllib.error as ftperror, shutil, logging
from pathlib import Path
path = Path(__file__).resolve()
default_save_dir = path.parent.parent.absolute() / "files"
logger = logging.getLogger(__name__)

"""
Function to download a single file based on ftp protocol

Parameters:
    url (str): 
        FTP URL to download from
    dir_to_save (str):
        Path of the directory to save the downloaded files

    Returns:
        bool: Boolean to indicate whether the file has been successfully downloaded
"""
def download_file(url: str, dir_to_save: str = default_save_dir) -> bool:
    current_disk_space = get_current_disk_space()

    try:
        r = ftprequest.urlopen(url)
        expected_file_size = int(r.info()['Content-Length'], 0)
        logger.info(f"Size of {url}: {convert_size(expected_file_size)}")
    except ftperror.HTTPError as e:
        logger.info(e.__dict__)
        raise e.__dict__
    except ftperror.URLError as e:
        logger.info(e.__dict__)
        raise e.__dict__
    
    if current_disk_space >= expected_file_size:
        # Open the FTP connection
        local_filename = url.split('/')[-1]
        path_to_save = unique_file(Path(dir_to_save) / local_filename)

        logger.info(f"Saving {url} at {path_to_save}")
        with closing(ftprequest.urlopen(url)) as r:
            with open(path_to_save, 'wb') as f:
                shutil.copyfileobj(r, f)

        return check_file_size(expected_file_size, url, path_to_save)
    else:                
        logger.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
        raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
