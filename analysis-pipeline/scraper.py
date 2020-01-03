
import csv
import requests
import re
import os
from multiprocessing import Queue
from threading import Thread
import sys

concurrent = 200

def check_dir_exists(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)

def scrape_url():
  while True:
    try:
      url = q.get()
      r = requests.get(url, allow_redirects=True)
      d = r.headers['content-disposition']
      fname = re.findall("filename=(.+)", d)[0]
      open(os.path.join("scraper_output/", fname.lstrip("\"").rstrip("\"")), 'wb').write(r.content)
      # q.task_done()
    except Exception as e:
      print(e)

def parse_mal_urls(queue, file, tag):
  with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      if (tag in row['tags'] and row['url_status'] == "online"):
        queue.put(row["url"])
        
if __name__== "__main__" :
  q = Queue(concurrent)
  check_dir_exists("scraper_output/")
  for i in range(concurrent):
      t = Thread(target=scrape_url)
      t.daemon = True
      t.start()
  try:
    parse_mal_urls(q,"urls/mal_urls.csv", "emotet")
  except KeyboardInterrupt:
    sys.exit()