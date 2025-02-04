from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from check_appointment import check_appointment

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service("D:\\chromedriver\\chromedriver.exe")

city_map = {
  "Grønland": "c4afbbf5b8fea8ae5b5749370eaa26ae1c405797f39e8b6bfec5f3f96255451e",
  "Lillestrøm": "9362230d4803607d0f874f958a554d0d46642980c7917856a34fa46786acd48e",
  "Sandvika": "e8cfd353ad2e1f03432faa6d1c1ea3401102eb0bf7e8f9e9fe0e2607f867a8a0",
  "Ski": "b56db719fe3d46ba2d691e97b8dc58ff99bf66e93980ac01c0b88e7c386d7fac"
}

check_appointment(city_map, service, chrome_options, datetime(2025, 3, 15),
                  'SG.3CfdbYvHRVCDi08cKjRj0g.WRZz_',
                  'xxx@outlook.com', 'xxx@gmail.com')
