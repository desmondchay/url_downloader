from contextlib import closing
from pathlib import Path
import shutil, logging

import requests

from .util import get_current_disk_space, unique_file, check_file_size, convert_size

path = Path(__file__).resolve()
default_save_dir = path.parent.parent.absolute() / "files"
logger = logging.getLogger(__name__)

"""
Function to download a single file based on http protocol

Parameters:
    url (str): 
        HTTP URL to download from
    dir_to_save (str):
        Path of the directory to save the downloaded files

    Returns:
        bool: Boolean to indicate whether the file has been successfully downloaded
"""
def download_file(url: str, dir_to_save: str = default_save_dir) -> bool:
    current_disk_space = get_current_disk_space()
    try:
        response = requests.head(url)
        expected_file_size = int(response.headers['Content-length'], 0)
        logger.info(f"Size of {url}: {convert_size(expected_file_size)}")
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e
    
    if current_disk_space >= expected_file_size:
        local_filename = url.strip('/').split('/')[-1]
        with closing(requests.get(url, stream=True, verify=True)) as r:
            try:
                path_to_save = unique_file(Path(dir_to_save) / local_filename)
                logger.info(f"Saving {url} at {path_to_save}")
                with closing(open(path_to_save, 'wb')) as f:
                    shutil.copyfileobj(r.raw, f)
            except requests.exceptions.RequestException as e:
                logger.error(e)
                raise e

        return check_file_size(expected_file_size, url, path_to_save)
    else:                
        logger.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
        raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")