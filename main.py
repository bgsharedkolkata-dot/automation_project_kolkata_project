import threading
import requests
from bs4 import BeautifulSoup
import sqlite3
from tqdm import tqdm
from queue import Queue
import time

# ---------- CONFIGURATION ----------
URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.bbc.com",
    "https://www.nytimes.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.reddit.com",
    "https://www.cnn.com",
    "https://www.medium.com"
] * 3  # replicate to simulate more work

NUM_WORKERS = 5
DB_NAME = "scraped_data.db"
# -----------------------------------


# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            url TEXT PRIMARY KEY,
            title TEXT
        )
    ''')
    conn.commit()
    conn.close()
# -------------------------------------


# ---------- SCRAPER WORKER ----------
def scrape_worker(queue, progress):
    while not queue.empty():
        url = queue.get()
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.string.strip() if soup.title else "No Title Found"
            save_to_db(url, title)
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
        finally:
            progress.update(1)
            queue.task_done()
# -------------------------------------


# ---------- SAVE TO DB ----------
def save_to_db(url, title):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO pages (url, title) VALUES (?, ?)", (url, title))
        conn.commit()
    finally:
        conn.close()
# ----------------------------------


# ---------- MAIN RUNNER ----------
def run_scraper():
    init_db()

    task_queue = Queue()
    for url in URLS:
        task_queue.put(url)

    progress = tqdm(total=task_queue.qsize(), desc="Scraping")

    threads = []
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=scrape_worker, args=(task_queue, progress))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    progress.close()
    print("✅ Scraping complete. Data saved to:", DB_NAME)
# ----------------------------------

if __name__ == "__main__":
    start_time = time.time()
    run_scraper()
    print(f"⏱️ Total time taken: {time.time() - start_time:.2f} seconds")
