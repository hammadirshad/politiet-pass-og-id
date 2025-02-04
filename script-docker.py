from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from check_appointment import check_appointment

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

service = Service(
    executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver")

city_map = {
  "Grønland": "c4afbbf5b8fea8ae5b5749370eaa26ae1c405797f39e8b6bfec5f3f96255451e",
  "Lillestrøm": "9362230d4803607d0f874f958a554d0d46642980c7917856a34fa46786acd48e",
  "Sandvika": "e8cfd353ad2e1f03432faa6d1c1ea3401102eb0bf7e8f9e9fe0e2607f867a8a0"
}
check_appointment(city_map, service, chrome_options)
