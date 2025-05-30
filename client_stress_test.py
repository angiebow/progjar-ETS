from concurrent.futures import ThreadPoolExecutor
import time
from file_client_cli import remote_upload 

def worker_upload(filename):
    start = time.time()
    success = remote_upload(filename)  # fungsi dari tugas 3
    end = time.time()
    return success, end-start

jumlah_worker = 5  

executor = ThreadPoolExecutor(max_workers=jumlah_worker)
futures = [executor.submit(worker_upload, 'test10mb.zip') for _ in range(jumlah_worker)]

for future in futures:
    result, duration = future.result()