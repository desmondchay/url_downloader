from downloader.ftp import download_file
import unittest
from pathlib import Path
# from downloader import http, ftp, sftp
from downloader.http import download_file as download_http_file
from downloader.ftp import download_file as download_ftp_file
from downloader.sftp import download_file as download_sftp_file

test_path = Path(__file__).resolve().parent.absolute()

class TestPortocolDownloader(unittest.TestCase):
    def test_http_downloader(self):
        url = "http://speedtest.tele2.net/1MB.zip"
        res = download_http_file(url, test_path)

        self.assertEqual(res, True)
        Path(test_path / url.split('/')[-1]).unlink(missing_ok=True)

    def test_ftp_downloader(self):
        url = "ftp://speedtest.tele2.net/100KB.zip"
        res = download_ftp_file(url, test_path)

        self.assertEqual(res, True)
        Path(test_path / url.split('/')[-1]).unlink(missing_ok=True)

    def test_sftp_downloader(self):
        path = "/pub/example/readme.txt"
        res = download_sftp_file("test.rebex.net","demo","password","22",path, test_path)
        
        self.assertEqual(res, True)
        Path(test_path / path.split('/')[-1]).unlink(missing_ok=True)

if __name__ == '__main__':
    unittest.main()