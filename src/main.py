from pathlib import Path
import logging, concurrent.futures
from client.ftp import download_file as download_ftp_file 
from client.http import download_file as download_http_file
from client.sftp import download_file as download_sftp_file
from util.util import get_url_links

path = Path(__file__).resolve()
folder_to_save = path.parent.parent.absolute()

num_max_workers = 5
urls_to_download_dir = path.parent.parent.absolute() / "config"
default_save_dir = path.parent.parent.absolute() / "files"

def batch_download_urls(protocol_func, csv_file_path):
    urls_to_download = get_url_links(urls_to_download_dir / csv_file_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        if isinstance(urls_to_download[0], dict):
            future_to_url = {executor.submit(protocol_func, url["host"], url["username"], url["password"], url["port"], url["path"]) : url for url in urls_to_download}
        else:
            future_to_url = {executor.submit(protocol_func, url): url for url in urls_to_download}
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
        
if __name__ == '__main__':
    
    path = Path(__file__).resolve()
    folder_to_save = path.parent.parent.absolute()
    filename= "log.log"
    logging.basicConfig(filename= folder_to_save / filename, filemode = 'a', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
    
    batch_download_urls(download_sftp_file, "sftp_urls.csv")
    batch_download_urls(download_http_file, "http_urls.csv")
    batch_download_urls(download_ftp_file, "ftp_urls.csv")