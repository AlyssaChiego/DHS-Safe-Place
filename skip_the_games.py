import datetime
import time
import pandas as pd
import undetected_chromedriver
import ssl

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

ssl._create_default_https_context = ssl._create_unverified_context
timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
LIST = []
url = 'https://skipthegames.com/posts/fort-myers'

headers = {
    'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54'
}
# SET UP HEADLESS PAGE
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# driver = undetected_chromedriver.Chrome(options=options)
driver = undetected_chromedriver.Chrome()
driver.implicitly_wait(60)

driver.get(url)
time.sleep(5)
LIST = []

# WAIT FOR ELEMENTS TO BE CLICKABLE
wait = WebDriverWait(driver, 10)

# LIST FOR KEYWORDS
keywords = [
    "no cops",
    "woman",
    "escort",
    "young",
    "phone number",
    "no police",
    "law enforcement",
    "discreet location",
    "snap chat",
    "snapchat",
    "e$cort",
    "baby"
]

driver.refresh()
# ACCEPT COOKIES
cookie = driver.find_element(By.CLASS_NAME, 'cc-cookie-accept')
driver.execute_script("arguments[0].click();", cookie)
driver.implicitly_wait(10)

# SELECT PREFERENCES
# SELF-IDENTIFICATION (MALE, WOMAN, ETC.)
identification = Select(driver.find_element(By.NAME, 'input_search_client'))
identification.select_by_value('men')
driver.implicitly_wait(10)

# LOOKING FOR: ESCORT,
category = Select(driver.find_element(By.NAME, 'input_search_category'))
category.select_by_value('female-escorts')
driver.implicitly_wait(10)


driver.refresh()
posts = driver.find_elements(By.CSS_SELECTOR, 'html.no-js body div table.two-col-wrap tbody tr '
                             'td#gallery_view.listings-with-sidebar.list-search-results.gallery div.full-width '
                             'div.small-16.columns div.clsfds-display-mode.gallery div.day-gallery [href]')
dupLinks = [post.get_attribute('href') for post in posts]
links = [*set(dupLinks)]
counter = 0
for urls in links:
    driver.get(links[counter])
    counter += 1

    ad_url = driver.current_url
    print(ad_url)

    title = driver.find_element(By.CLASS_NAME, 'post-title').text
    print(title)

    # APPEND CONTENTS TO LIST
    LIST.append([ad_url, title])

    # SCREENSHOT LISTING
    screenshot_name = f"skipthegames{[counter]}.png"
    driver.save_screenshot(screenshot_name)


# SET SCREENSHOT SIZE
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'), S('Height'))

# SET UP COLUMNS FOR EXCEL FILE
columns = ('URL', 'Title')
df = pd.DataFrame(LIST, columns=columns)

# EXPORT TO EXCEL FILE
df.to_excel(f'skipthegames({timestamps}).xlsx', index=False)
print(f'skipthegames({timestamps}).xlsx exported.')

# CLOSE WEBDRIVER
driver.close()