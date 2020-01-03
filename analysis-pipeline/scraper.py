
import csv
import requests
import re
import os

def check_dir_exists(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)

def scrape_url(url, output_dir):
  try:
    r = requests.get(url, allow_redirects=True)
    d = r.headers['content-disposition']
    fname = re.findall("filename=(.+)", d)[0]
    print (fname.lstrip("\"").rstrip("\""))
    open(os.path.join(output_dir, fname.lstrip("\"").rstrip("\"")), 'wb').write(r.content)
  except Exception as e:
    print(e)


def parse_mal_urls(file, tag, output_dir='scraper_output/'):
  # emotet_dict = {}
  check_dir_exists(output_dir)
  with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      if (tag in row['tags'] and row['url_status'] == "online"):
        scrape_url(row["url"], output_dir)
        
if __name__== "__main__" :
  parse_mal_urls("urls/mal_urls.csv", "emotet")
