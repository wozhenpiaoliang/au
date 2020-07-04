from concurrent.futures.thread import ThreadPoolExecutor

MAX_THREAD_WORKERS = 64
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS)