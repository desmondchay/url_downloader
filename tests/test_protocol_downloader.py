import unittest
from pathlib import Path

from downloader.http import download_file as download_http_file
from downloader.ftp import download_file as download_ftp_file
from downloader.sftp import download_file as download_sftp_file
from downloader.batch_download import batch_download_urls
from downloader.util import unique_file

test_path = Path(__file__).resolve().parent.absolute()

class TestPortocolDownloader(unittest.TestCase):
    def test_http_downloader(self):
        url = "http://speedtest.tele2.net/1MB.zip"
        local_filename = url.strip('/').split('/')[-1]
        path_to_save = unique_file(Path(test_path) / local_filename)
        res = download_http_file(url, test_path)

        self.assertEqual(res, True)
        Path(path_to_save).unlink(missing_ok=True)

    def test_https_downloader(self):
        url = "https://www.lifewire.com/thmb/RWgG0dGcpgZENOnoONDalJPgneA=/853x640/smart/filters:no_upscale()/png-file-photos-app-5b75972f46e0fb002c692c03.png"
        local_filename = url.strip('/').split('/')[-1]
        path_to_save = unique_file(Path(test_path) / local_filename)
        res = download_http_file(url, test_path)

        self.assertEqual(res, True)
        Path(path_to_save).unlink(missing_ok=True)

    def test_ftp_downloader(self):
        url = "ftp://speedtest.tele2.net/100KB.zip"
        local_filename = url.strip('/').split('/')[-1]
        path_to_save = unique_file(Path(test_path) / local_filename)
        res = download_ftp_file(url, test_path)

        self.assertEqual(res, True)
        Path(path_to_save).unlink(missing_ok=True)

    def test_sftp_downloader(self):
        path = "/pub/example/readme.txt"
        local_filename = path.strip('/').split('/')[-1]
        path_to_save = unique_file(Path(test_path) / local_filename)
        res = download_sftp_file("test.rebex.net","demo","password","22",path, test_path)
        
        self.assertEqual(res, True)
        Path(path_to_save).unlink(missing_ok=True)

    def test_batch_downloader(self):
        csv_file_path = test_path.parent / "config/http_urls.csv"
        batch_download_urls(download_http_file, csv_file_path, test_path)

        self.assertEqual(Path(test_path / "1MB.zip").exists(), True)
        self.assertEqual(Path(test_path / "10MB.zip").exists(), True)
        self.assertEqual(Path(test_path / "info.cern.ch").exists(), True)
        self.assertEqual(Path(test_path / "png-file-photos-app-5b75972f46e0fb002c692c03.png").exists(), True)

        # remove downloaded files
        Path(test_path / "1MB.zip").unlink(missing_ok=True)
        Path(test_path / "10MB.zip").unlink(missing_ok=True)
        Path(test_path / "info.cern.ch").unlink(missing_ok=True)
        Path(test_path / "png-file-photos-app-5b75972f46e0fb002c692c03.png").unlink(missing_ok=True)

if __name__ == '__main__':
    unittest.main()