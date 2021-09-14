---
## URL Downloader
---
## Project details
URL Downloader is a python module/script that allows users to download files from multiple protocols.
Users may download files over the http, https, ftp, sftp protocols either using functions defined in the module or
using the python script defined in `main.py`

## Setup without docker
1. Navigate to root folder
2. Install dependencies with `pip install -r requirements.txt`
3. Run a python shell within the src directory and use the defined modules accordingly

## Setup with docker
1. Navigate to root folder
2. Build docker image with `docker build -t url_downloader .`
3. Setup the urls you wish to retrieve as per instructions above
4. Define a DIR_TO_SAVE_FILES where you wish to store the downloaded files
5. Run docker container with `docker run -it --mount type=bind,source={DIR_TO_SAVE_FILES},target=/app/files --mount type=bind,source={DIR_FOR_BATCH_DOWNLOAD_REF},target=/app/config url_downloader` python
6. Note that usage will differ since the file system within the Docker container is structured differently

## Usage
### Downloading single url with defined functions for different protocols
```
# downloading single url example
from downloader.http import download_file as download_http_file
from downloader.ftp import download_file as download_ftp_file
from downloader.sftp import download_file as download_sftp_file
download_http_file("http://speedtest.tele2.net/1MB.zip")
download_ftp_file("ftp://speedtest.tele2.net/1KB.zip")
download_sftp_file("test.rebex.net","demo","password","22","/pub/example/readme.txt")

# downloading single url with specified save path
download_http_file("http://speedtest.tele2.net/1MB.zip", "C:/Users/desmond/Desktop/downloaded")
```

###  Batch downloading a list of urls with defined functions for different protocols
1. Define urls that you wish to obtain in batch within the `config` directory
2. An example format is as below:

#### For `config/http_urls.csv` or `config/ftp_urls.csv`
|  urls                               |
| :-----------------------------------|
|  http://google.com                  |
|  http://speedtest.tele2.net/1MB.zip |
|  http://speedtest.tele2.net/10MB.zip|
|  http://info.cern.ch/               |

#### For `config/sftp_urls.csv`
|  host           |  username    |  password |  port |  path                    |
| :---------------| :------------| :---------| :-----| :------------------------|
|  test.rebex.net |  "demo"      | password  | 22    | "/pub/example/readme.txt"|

```
# downloading in batch example
from downloader.batch_download import batch_download_urls
from downloader.http import download_file as download_http_file

# download in batch with specified path to read the urls to download
batch_download_urls(protocol_func = download_http_file, csv_file_path= "C:/Users/desmond/Desktop/agoda/config/http_urls.csv")
# download in batch with specified path to read the urls to download within docker container
batch_download_urls(protocol_func = download_http_file, csv_file_path= "app/downloader/configs/your_csv_name.csv")

# downloading in batch with specified save path
batch_download_urls(protocol_func = download_http_file, csv_file_path = "C:/Users/desmond/Desktop/urls/urls.csv", dir_to_save = "C:/Users/desmond/Desktop/downloaded")
```

### Using a real-time CLI for files with http/https protocol 
1. Run the script with `python downloader/main.py` while in the root folder
2. Enter any http/https protocol supported url
3. The script will update on the progress of any submitted downloads after each input
4. When specifying exit, the script will also check on any ongoing downloads and allow the user to handle them

## Run unit tests
```
# run tests
python -m unittest discover
```

## External Python libraries used
- requests (for http)
- paramiko (for sftp)