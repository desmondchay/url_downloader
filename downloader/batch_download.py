from pathlib import Path
from typing import Callable
import logging, concurrent.futures

from .util import get_url_links

num_max_workers = 5
root_path = Path(__file__).resolve().parent.parent.absolute()
default_save_dir = root_path / "files"
logger = logging.getLogger(__name__)

"""
Function to batch download a list of files with links defined in a csv, with a defined protocol function

Parameters:
    protocol_func (Callable): 
        Function that uses underlying python libraries which supports the protocol in downloading the file
    csv_file_path (str): 
        Path of the csv file to reference which files should be downloaded
    dir_to_save (str):
        Path of the directory to save the downloaded files
"""
def batch_download_urls(protocol_func: Callable, csv_file_path: str, dir_to_save: str = default_save_dir) -> None:
    urls_to_download = get_url_links(csv_file_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        if isinstance(urls_to_download[0], dict):
            future_to_url = {executor.submit(protocol_func, url["host"], url["username"], url["password"], url["port"], url["path"], dir_to_save) : url for url in urls_to_download}
        else:
            future_to_url = {executor.submit(protocol_func, url, dir_to_save): url for url in urls_to_download}
        for future in concurrent.futures.as_completed(future_to_url):
            if isinstance(future_to_url[future], dict):
                url = future_to_url[future]["path"]
            else:
                url = future_to_url[future]
            try:
                is_success = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                if is_success:
                    print(f"{url} downloaded successfully")
                else:
                    print(f"{url} download failed")
