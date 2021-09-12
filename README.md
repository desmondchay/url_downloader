---
## URL Downloader
---

## Setup with docker
1. Navigate to root folder
2. Build docker image with `docker build -t url_downloader .`
3. Setup the urls you wish to retrieve as per instructions above
4. Define a DIR_TO_SAVE_FILES where you wish to store the downloaded files
5. Run docker container with `docker run -it --mount type=bind,source={DIR_TO_SAVE_FILES},target=/app/files --mount type=bind,source={DIR_TO_CHANGE_CONFIGS},target=/app/config url_downloader` python

## Setup without docker
1. Navigate to root folder
2. Install dependencies with `pip install -r requirements.txt`
3. Run a python shell within the src directory and use the defined modules accordingly

### Usage
#### Downloading single url with defined functions for different protocols
```
# downloading single url example
from client.http import download_file as download_http_file
from client.ftp import download_file as download_ftp_file
from client.sftp import download_file as download_sftp_file
download_http_file("http://speedtest.tele2.net/1MB.zip")
download_ftp_file("ftp://speedtest.tele2.net/1KB.zip")
download_sftp_file("test.rebex.net","demo","password","22","/pub/example/readme.txt")

# downloading single url with specified save path
download_http_file("http://speedtest.tele2.net/1MB.zip", "PATH")
```

####  Batch downloading a list of urls with defined functions for different protocols
1. Define urls that you wish to obtain in batch within the `config` directory
2. An example format is as below:

##### For `config/http_urls.csv` or `config/ftp_urls.csv`
|  urls                               |
| :-----------------------------------|
|  http://google.com                  |
|  http://speedtest.tele2.net/1MB.zip |
|  http://speedtest.tele2.net/10MB.zip|
|  http://info.cern.ch/               |

##### For `config/sftp_urls.csv`
|  host           |  username    |  password |  port |  path                    |
| :---------------| :------------| :---------| :-----| :------------------------|
|  test.rebex.net |  "demo"      | password  | 22    | "/pub/example/readme.txt"|

```
# downloading in batch example
from main import batch_download_urls
from client.http import download_file as download_http_file

batch_download_urls(download_http_file, "http_urls.csv")

# downloading in batch with specified save path
batch_download_urls(download_http_file, "http_urls.csv", "PATH_to_save")
```

## Run unit tests
TBD
