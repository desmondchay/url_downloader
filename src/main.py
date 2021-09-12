from pathlib import Path
import logging, concurrent.futures
from util.util import get_url_links
from typing import Callable

num_max_workers = 5
path = Path(__file__).resolve()
root_path = path.parent.parent.absolute()

urls_to_download_dir = root_path / "config"
default_save_dir = root_path / "files"

log_path = root_path / "log.log"
logging.basicConfig(filename= log_path, filemode = 'a', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
    
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
    urls_to_download = get_url_links(urls_to_download_dir / csv_file_path)
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
