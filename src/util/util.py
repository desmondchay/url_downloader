import shutil, math, logging, csv
from pathlib import Path
from itertools import count
logger = logging.getLogger(__name__)

def get_current_disk_space():
    free_disk_space = shutil.disk_usage("/").free
    logger.info(f"Current disk space: {convert_size(free_disk_space)}")
    return free_disk_space

def unique_file(path):
    ext = Path(path).suffix
    basename = Path(path).parents[0] / Path(path).stem
    actualname = path
    c = count(start = 1)
    while Path(actualname).exists():
        actualname = "%s (%d).%s" % (basename, next(c), ext)
    return actualname

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

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def check_file_size(expected_file_size, download_path, saved_path):
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
