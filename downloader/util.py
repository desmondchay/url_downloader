from pathlib import Path
from itertools import count
import shutil, math, logging, csv

logger = logging.getLogger(__name__)

"""
Function to get the current remaining disk space on the client

    Returns:
        int: amount of free disk space in bytes
"""
def get_current_disk_space() -> int:
    free_disk_space = shutil.disk_usage("/").free
    logger.info(f"Current disk space: {convert_size(free_disk_space)}")
    return free_disk_space

"""
Function to rename the local name of the downloaded file if another file exists with the same name

    Parameters:
        path (str):
            The local path where we are initially saving the downloaded file at
    Returns:
        str: the actual local path we should be saving the downloaded file as
"""
def unique_file(path: str) -> str:
    ext = Path(path).suffix
    basename = Path(path).parents[0] / Path(path).stem
    actualname = path
    c = count(start = 1)
    while Path(actualname).exists():
        actualname = "%s (%d).%s" % (basename, next(c), ext)
    return actualname

"""
Function to parse through the given csv files and return a list of rows for the parameters that we should be passing into download functions

    Parameters:
        filepath (str):
            The local path where we store the csv file that stores the information to download the urls at
    Returns:
        list: a list of parameters to pass into the specified download function
"""
def get_url_links(filepath: str) -> list:
    try:
        with open(filepath) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            header = next(reader, None)
            if header and len(header) == 1:
                return [row[0] for row in reader]
            elif header and len(header) > 1:
                res = []
                for row in reader:
                    dict_res = {}
                    for i,v in enumerate(row):
                        dict_res[header[i]] = v
                    res.append(dict_res)
                return res
            else:
                raise ValueError(f"Expected headers in {filepath} but did not find")
    except FileNotFoundError as e:  
        raise e

"""
Function to convert the raw byte size into a human readable byte format

    Parameters:
        size_bytes (int):
            The raw byte value
    Returns:
        str: Human readable byte format
"""
def convert_size(size_bytes: int) -> str:
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


"""
Function to check if the local downloaded file has the same size that is specified in the content header of the URL given

    Parameters:
        expected_file_size (int):
            The file size in bytes where we expect to save, given by the content headers for http protocol urls
        download_path (str):
            URL to fetch the file from, passed simply for logging purposes
        saved_path (int):
            Local path where the downloaded file is saved at
    Returns:
        bool: True if the file size is the same, False otherwise
"""
def check_file_size(expected_file_size: int, download_path: str, saved_path: str) -> bool:
        if expected_file_size > 0:
            if expected_file_size == Path(saved_path).stat().st_size:
                logger.info(f"{download_path} successfully saved at {saved_path}")
                return True
            else:
                logger.info(f"Download for {download_path} failed")
                Path(saved_path).unlink(missing_ok=True)
                return False
        else:
            logger.info(f"Unable to validate if {saved_path.split('/'[-1])} is downloaded successfully, please do a manual check at {saved_path}")    
