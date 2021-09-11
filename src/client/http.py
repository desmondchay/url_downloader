from util.util import get_current_disk_space, unique_file, check_file_size, convert_size
from contextlib import closing
import requests, shutil, logging
from pathlib import Path
path = Path(__file__).resolve()
default_save_dir = path.parent.parent.parent.absolute() / "files"
logger = logging.getLogger(__name__)

def download_file(url, dir_to_save = default_save_dir):
    current_disk_space = get_current_disk_space()
    try:
        response = requests.head(url)
        expected_file_size = int(response.headers['Content-length'], 0)
        logger.info(f"Size of {url}: {convert_size(expected_file_size)}")
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e
    
    if current_disk_space >= expected_file_size:
        if url.split('/')[-1]:
            local_filename = url.split('/')[-1]
        else:
            local_filename = "url"
        with closing(requests.get(url, stream=True)) as r:
            if r.status_code == requests.codes.ok:
                path_to_save = unique_file(dir_to_save / local_filename)
                logger.info(f"Saving {url} at {path_to_save}")
                with closing(open(path_to_save, 'wb')) as f:
                    shutil.copyfileobj(r.raw, f)

        return check_file_size(expected_file_size, url, path_to_save)
    else:                
        logger.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
        raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")