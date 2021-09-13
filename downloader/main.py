import sys
from pathlib import Path 
file_path = Path(__file__).resolve()
parent_path, root_path = file_path.parent, file_path.parents[1]
sys.path.append(str(root_path))

try:
    sys.path.remove(str(parent_path))
except ValueError:
    pass

import queue
q = queue.Queue()

import concurrent.futures
from downloader.http import download_file as download_http_file
# from downloader.ftp import download_file as download_ftp_file
# from downloader.sftp import download_file as download_sftp_file

future_to_url = {}

import signal, psutil, os

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            url = input("Welcome, please enter http/https url to fetch, else type in exit to terminate safely: ")
            if url == "exit":
                not_done = concurrent.futures.wait(future_to_url, timeout=0.1,return_when=concurrent.futures.FIRST_COMPLETED).not_done
                for future in not_done:
                    url = future_to_url[future]
                    confirmation = input(f"{url} is still being fetched, do you want to wait for it to finish? (yes/no): ")
                    if confirmation == "no":
                        break
                    elif confirmation == "yes":
                        try:
                            is_success = future.result()
                            if is_success:
                                print(f"{url} downloaded successfully")
                            else:
                                print(f"Download for {url} failed")
                        except Exception as exc:
                            print('%r generated an exception: %s' % (url, exc))  
                print("Shutting down gracefully...")
                # Kill remaining child processes
                kill_child_processes(os.getpid())
                executor.shutdown(wait=False)
                break
            
            task = executor.submit(download_http_file, url)
            future_to_url[task] = url
            
            done, not_done = concurrent.futures.wait(future_to_url, timeout=0.1,return_when=concurrent.futures.FIRST_COMPLETED)
            if future_to_url:
                for future in done:
                    url = future_to_url[future]
                    try:
                        is_success = future.result()
                        if is_success:
                            print(f"{url} downloaded successfully")
                        else:
                            print(f"Download for {url} failed")
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))  
                    # remove the now completed future
                    del future_to_url[future]
                for future in not_done:
                    print(f"{future_to_url[future]} is still in progress")