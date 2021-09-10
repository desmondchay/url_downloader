from pathlib import Path
import requests
import shutil
import math
import logging
import urllib.request as ftprequest
import urllib.error as ftperror
from contextlib import closing
import csv
import itertools
import concurrent.futures
import paramiko

path = Path(__file__).resolve()
folder_to_save = path.parent.parent.absolute()
filename= "log.log"
logging.basicConfig(filename= folder_to_save / filename, filemode = 'a', level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def download_file(url):
    path = Path(__file__).resolve()
    local_path = path.parent.parent.absolute() / "files"

    logging.info(f"Current disk space: {convert_size(get_current_disk_space())}")
    expected_file_size = get_file_size(url)
    logging.info(f"Size of {url}: {convert_size(expected_file_size)}")
    
    if get_current_disk_space() >= expected_file_size:
        if url.split('/')[-1]:
            local_filename = url.split('/')[-1]
        else:
            local_filename = "url"
        with closing(requests.get(url, stream=True)) as r:
            if r.status_code == requests.codes.ok:
                path_to_save = unique_file(local_path / local_filename)
                logging.info(f"Saving {url} at {path_to_save}")
                with closing(open(path_to_save, 'wb')) as f:
                    shutil.copyfileobj(r.raw, f)

        if expected_file_size>0:
            if expected_file_size == Path(path_to_save).stat().st_size:
                logging.info(f"{url} successfully saved at {path_to_save}")
                return True
            else:
                logging.info(f"Download for {url} failed")
                Path(path_to_save).unlink(missing_ok=True)
                return False
        else:
            logging.info(f"Unable to validate if {url} is downloaded successfully, please do a manual check at {path_to_save}")
    else:                
        logging.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")
        raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")


def get_file_size(url):
    try:
        response = requests.head(url)
        return int(response.headers['Content-length'], 0)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise e
        
def get_current_disk_space():
    return int(shutil.disk_usage("/").free)

def unique_file(path):
    ext = Path(path).suffix
    basename = Path(path).parents[0] / Path(path).stem
    actualname = path
    c = itertools.count(start = 1)
    while Path(actualname).exists():
        actualname = "%s (%d).%s" % (basename, next(c), ext)
    return actualname

def download_ftp_file(url):
    path = Path(__file__).resolve()
    local_path = path.parent.parent.absolute() / "files"

    logging.info(f"Current disk space: {convert_size(get_current_disk_space())}")
    expected_file_size = get_ftp_file_size(url)
    logging.info(f"Size of {url}: {convert_size(expected_file_size)}")
    
    if get_current_disk_space() >= expected_file_size:
        # Open the FTP connection
        local_filename = url.split('/')[-1]
        path_to_save = unique_file(local_path / local_filename)

        logging.info(f"Saving {url} at {path_to_save}")
        with closing(ftprequest.urlopen(url)) as r:
            with open(path_to_save, 'wb') as f:
                shutil.copyfileobj(r, f)

        if expected_file_size > 0:
            if expected_file_size == Path(path_to_save).stat().st_size:
                logging.info(f"{url} successfully saved at {path_to_save}")
                return True
            else:
                logging.info(f"Download for {url} failed")
                Path(path_to_save).unlink(missing_ok=True)
                return False
        else:
            logging.info(f"Unable to validate if {url} is downloaded successfully, please do a manual check at {path_to_save}")

    else:                
        logging.exception(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")
        raise OSError(f"Not enough space on system to save {url}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")


def get_ftp_file_size(url):
    try:
        r = ftprequest.urlopen(url)
        return int(r.info()['Content-Length'], 0)
    except ftperror.HTTPError as e:
        logging.info(e.__dict__)
        raise e.__dict__
    except ftperror.URLError as e:
        logging.info(e.__dict__)
        raise e.__dict__

def get_url_links(filepath):
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

def download_sftp_file(host, username, password, port, download_path):
    local_path = Path(__file__).resolve().parent.parent.absolute() / "files"

    transp = paramiko.Transport((host,int(port)))
    transp.connect(username=username,password=password)
    client = paramiko.SFTPClient.from_transport(transp)
    expected_file_size = client.stat(download_path).st_size

    if get_current_disk_space() >= expected_file_size:
        local_filename = download_path.split('/')[-1]
        path_to_save = unique_file(local_path / local_filename)

        logging.info(f"Saving {download_path} at {path_to_save}")
        try:
            with client as host:
                sftp_file_instance = host.open(download_path, 'r')
                with open(path_to_save, 'wb') as out_file:
                    shutil.copyfileobj(sftp_file_instance, out_file)

            if expected_file_size > 0:
                if expected_file_size == Path(path_to_save).stat().st_size:
                    logging.info(f"{download_path} successfully saved at {path_to_save}")
                    return True
                else:
                    logging.info(f"Download for {download_path} failed")
                    Path(path_to_save).unlink(missing_ok=True)
                    return False
            else:
                logging.info(f"Unable to validate if {download_path} is downloaded successfully, please do a manual check at {path_to_save}")
        except Exception as e:
            logging.exception(e)
            raise e
    else:
        client.close()                
        logging.exception(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")
        raise OSError(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(get_current_disk_space())}")

if __name__ == '__main__':
    path = Path(__file__).resolve()
    local_path = path.parent.parent.absolute() / "config"

    http_urls_to_download = get_url_links(local_path / "http_urls.csv")
    ftp_urls_to_download = get_url_links(local_path / "ftp_urls.csv")
    sftp_urls_to_download = get_url_links(local_path / "sftp_urls.csv")

    num_max_workers = 5

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        http_future_to_url = {executor.submit(download_file, url): url for url in http_urls_to_download}
        ftp_future_to_url = {executor.submit(download_ftp_file, url): url for url in ftp_urls_to_download}
        sftp_future_to_url = {executor.submit(download_sftp_file, url["host"], url["username"], url["password"], url["port"], url["path"]) : url for url in sftp_urls_to_download}
        futures = ftp_future_to_url | http_future_to_url | sftp_future_to_url
        for future in concurrent.futures.as_completed(futures):
            if isinstance(futures[future], dict):
                url = futures[future]["path"]
            else:
                url = futures[future]
            try:
                is_success = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                if is_success:
                    print(f"{url} downloaded successfully")
                else:
                    print(f"{url} download failed")

    