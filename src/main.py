from pathlib import Path
from contextlib import closing
import shutil, logging, concurrent.futures
from client.ftp import download_file as download_ftp_file 
from client.http import download_file as download_http_file
from client.sftp import download_file as download_sftp_file
from util.util import get_url_links

path = Path(__file__).resolve()
folder_to_save = path.parent.parent.absolute()
logger = logging.getLogger(__name__)

num_max_workers = 5
urls_to_download_dir = path.parent.parent.absolute() / "config"
default_save_dir = path.parent.parent.absolute() / "files"

# def download_http_file(url, default_save_dir = default_save_dir):
#     current_disk_space = get_current_disk_space()
#     try:
#         response = requests.head(url)
#         expected_file_size = int(response.headers['Content-length'], 0)
#         logger.info(f"Size of {url}: {convert_size(expected_file_size)}")
#     except requests.exceptions.RequestException as e:
#         logger.error(e)
#         raise e
    
#     if current_disk_space >= expected_file_size:
#         if url.split('/')[-1]:
#             local_filename = url.split('/')[-1]
#         else:
#             local_filename = "url"
#         with closing(requests.get(url, stream=True)) as r:
#             if r.status_code == requests.codes.ok:
#                 path_to_save = unique_file(default_save_dir / local_filename)
#                 logger.info(f"Saving {url} at {path_to_save}")
#                 with closing(open(path_to_save, 'wb')) as f:
#                     shutil.copyfileobj(r.raw, f)

#         return check_file_size(expected_file_size, url, path_to_save)
#     else:                
#         logger.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
#         raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")

# def download_ftp_file(url, default_save_dir = default_save_dir):
#     current_disk_space = get_current_disk_space()

#     try:
#         r = ftprequest.urlopen(url)
#         expected_file_size = int(r.info()['Content-Length'], 0)
#         logger.info(f"Size of {url}: {convert_size(expected_file_size)}")
#     except ftperror.HTTPError as e:
#         logger.info(e.__dict__)
#         raise e.__dict__
#     except ftperror.URLError as e:
#         logger.info(e.__dict__)
#         raise e.__dict__
    
#     if current_disk_space >= expected_file_size:
#         # Open the FTP connection
#         local_filename = url.split('/')[-1]
#         path_to_save = unique_file(default_save_dir / local_filename)

#         logger.info(f"Saving {url} at {path_to_save}")
#         with closing(ftprequest.urlopen(url)) as r:
#             with open(path_to_save, 'wb') as f:
#                 shutil.copyfileobj(r, f)

#         return check_file_size(expected_file_size, url, path_to_save)
#     else:                
#         logger.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
#         raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")

# def download_sftp_file(host, username, password, port, download_path, default_save_dir = default_save_dir):
#     transp = paramiko.Transport((host,int(port)))
#     transp.connect(username=username,password=password)
#     client = paramiko.SFTPClient.from_transport(transp)
#     expected_file_size = client.stat(download_path).st_size
#     current_disk_space = get_current_disk_space()
#     if current_disk_space >= expected_file_size:
#         local_filename = download_path.split('/')[-1]
#         path_to_save = unique_file(default_save_dir / local_filename)

#         logger.info(f"Saving {download_path} at {path_to_save}")
#         try:
#             with client as host:
#                 sftp_file_instance = host.open(download_path, 'r')
#                 with open(path_to_save, 'wb') as out_file:
#                     shutil.copyfileobj(sftp_file_instance, out_file)

#             return check_file_size(expected_file_size, download_path, path_to_save)
#         except Exception as e:
#             logger.exception(e)
#             raise e
#     else:
#         client.close()                
#         logger.exception(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
#         raise OSError(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")

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