from util.util import get_current_disk_space, unique_file, check_file_size, convert_size
from contextlib import closing
import paramiko, shutil, logging
from pathlib import Path
path = Path(__file__).resolve()
default_save_dir = path.parent.parent.parent.absolute() / "files"
logger = logging.getLogger(__name__)

def download_file(host, username, password, port, download_path, dir_to_save = default_save_dir):
    transp = paramiko.Transport((host,int(port)))
    transp.connect(username=username,password=password)
    client = paramiko.SFTPClient.from_transport(transp)
    expected_file_size = client.stat(download_path).st_size
    current_disk_space = get_current_disk_space()
    if current_disk_space >= expected_file_size:
        local_filename = download_path.split('/')[-1]
        path_to_save = unique_file(dir_to_save / local_filename)

        logger.info(f"Saving {download_path} at {path_to_save}")
        try:
            with client as host:
                sftp_file_instance = host.open(download_path, 'r')
                with open(path_to_save, 'wb') as out_file:
                    shutil.copyfileobj(sftp_file_instance, out_file)

            return check_file_size(expected_file_size, download_path, path_to_save)
        except Exception as e:
            logger.exception(e)
            raise e
    else:
        client.close()                
        logger.exception(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
        raise OSError(f"Not enough space on system to save {download_path}. Require {convert_size(expected_file_size)}, remaining {convert_size(current_disk_space)}")
