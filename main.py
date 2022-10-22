import re
import sys
import time

import undetected_chromedriver as uc

# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

urls = [
    "https://1337x.to/torrent/2099267/Ubuntu-MATE-16-04-2-MATE-armhf-img-xz-Uzerus/",
    "https://thepiratebay.org/description.php?id=59191690",
    "https://idope.se/torrent/ubuntu/f1fcdc1462d36530f526c1d9402eec9100b7ba18/",
]


def extract_magnet_link(driver, url):

    magnet_link_with_trackers = ""

    driver.get(url)
    time.sleep(15)  # extra time for page load and CDN
    page_source = driver.page_source

    if url.startswith("https://1337x.to") or url.startswith("https://thepiratebay.org"):
        x = re.search(r'href="magnet:.xt=urn:btih:(.*?)"', page_source)
        if x is not None:
            magnet_link_with_trackers = f"magnet:?xt=urn:btih:{x.group(1)}"
    elif url.startswith("https://idope.se"):
        magnet_link = ""
        trackers = ""
        x = re.search(r'href="magnet:.xt=urn:btih:(.*?)"', page_source)
        if x is not None:
            magnet_infohash = x.group(1)
            magnet_link = f"magnet:?xt=urn:btih:{magnet_infohash.upper()}"
        x = re.search(r'id="hidetrack".*?value="(.*)"', page_source)
        if x is not None:
            trackers = x.group(1)
        if magnet_link and trackers:
            magnet_link_with_trackers = f"{magnet_link}{trackers}"
    else:
        # unsupported website
        pass
    return magnet_link_with_trackers


if __name__ == "__main__":
    print("starting")

    service = Service()
    if sys.platform.startswith("linux"):
        service.executable_path = "./chromedriver/Linux/106/chromedriver"
    elif sys.platform.startswith("win32"):
        service.executable_path = "./chromedriver/Windows/106/chromedriver.exe"
    else:
        print("unsupported system!")
        exit(1)

    options = Options()
    options.add_argument("--disable-gpu")  # required for dockerized Chrome
    # options.add_argument("--headless")
    options.add_argument("--incognito")  # optional
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    )  # any reasonable user agent will do

    # `undetected-chrome` helps to access websites sitting behind a CDN
    driver = uc.Chrome(
        service=service, options=options, use_subprocess=True
    )  # `use_subprocess=True` is required by `uc.Chrome()` but must be removed for `webservice.Chrome()`

    for url in urls:
        magnet_link = extract_magnet_link(driver, url)
        print(f"{url[0:35]} -- {magnet_link[0:55]}")

    print("stopping")
