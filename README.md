---
## URL Downloader
---
## Setup with docker
1. Define urls that you wish to download in a csv file. An example format is as below:
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

## Setup with docker
1. Navigate to root folder
2. Build docker image with `docker build -t url_downloader .`
3. Setup the urls you wish to retrieve as per instructions above
4. Define a DIR_TO_SAVE_FILES where you wish to store the downloaded files
5. Run docker container with `docker run -it --mount type=bind,source={DIR_TO_SAVE_FILES},target=/app/files --mount type=bind,source={DIR_TO_CHANGE_CONFIGS},target=/app/config url_downloader` python
6. Use `download_http_urls_from_csv`, `download_ftp_urls_from_csv`, `download_sftp_urls_from_csv` to enable batch downloads
7. Use `download_http_url(url)`, `download_ftp_url(url)`, `download_sftp_file(host, username, password, port, download_path)` to download a single file at a time

## Setup without docker
1. Navigate to root folder
2. Install dependencies with `pip install -r requirements.txt`
3. Define urls that you wish to obtain in `config/ftp_urls.csv, config/http_urls.csv, config/sftp_urls.csv`
4. Run the following.
```
# Run script
python src/main.py

```

## Run unit tests
TBD
