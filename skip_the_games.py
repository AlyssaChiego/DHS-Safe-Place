import datetime
import time
import pandas as pd
import undetected_chromedriver as uc
import ssl
import re
import pathlib
import selenium
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def run(selected_keywords):
    ssl._create_default_https_context = ssl._create_unverified_context
    timestamps = datetime.datetime.now().strftime('%m_%d_%y %H%M%S')
    LIST = []
    url = 'https://skipthegames.com/posts/fort-myers'

    headers = {
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/107.0.0.0 Safari/537.36',
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/108.0.0.0 Mobile Safari/537.36 Edg/108.0.1462.54'
    }

    # SET UP HEADLESS PAGE
    options = selenium.webdriver.ChromeOptions()
    chromedriver_autoinstaller.install()
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    driver.refresh()

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
                                                  'div.small-16.columns div.clsfds-display-mode.gallery '
                                                  'div.day-gallery ['
                                                  'href]')
    dupLinks = [post.get_attribute('href') for post in posts]
    links = [*set(dupLinks)]
    counter = 0

    for urls in links:
        print(f"Processing link {counter}: {urls}")  # Debugging print statement
        links[:] = (urls for urls in links if not urls.startswith('https://skipthegames.com/reply/meetup/'))
        driver.get(links[counter])
        time.sleep(5)

        description = driver.find_element(By.CSS_SELECTOR, '#post-body > div').text
        time.sleep(3)
        for keyword in selected_keywords:
            if keyword in description:
                ad_url = driver.current_url
                time.sleep(2)

                title = driver.find_element(By.CLASS_NAME, 'post-title').text
                time.sleep(2)
                pattern = r'(\(\d{3}\)\s*[-\.\s]\s*\d{3}\s*[-\.\s]??\s*\d{4}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{' \
                          r'3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'

                des = driver.find_element(By.CSS_SELECTOR, '#post-body > div').text
                phone_number = re.findall(pattern, des)
                time.sleep(2)
                # REMOVES DUPLICATES
                phone_number = [*set(phone_number)]

                # APPEND CONTENTS TO LIST
                LIST.append([counter, ad_url, title, phone_number, keyword])
                time.sleep(2)
                # SCREENSHOT LISTING
                screenshot_name = f"({counter})_{timestamps}_skipthegames.png"
                driver.save_screenshot(pathlib.Path.home() / f"Desktop/skipthegames/screenshots/{screenshot_name}")
                break

            # SET SCREENSHOT SIZE
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
            driver.set_window_size(S('Width'), S('Height'))

        counter += 1
    # SET UP COLUMNS FOR EXCEL FILE
    columns = ('Screenshot Number', 'URL', 'Title', 'Phone Number', 'Matching Keyword')
    df = pd.DataFrame(LIST, columns=columns)

    # EXPORT TO EXCEL FILE
    df.to_excel(pathlib.Path.home() / f"Desktop/skipthegames/excel_files/skipthegames({timestamps}).xlsx", index=False)
    print(f'skipthegames({timestamps}).xlsx exported.')
    # CLOSE WEBDRIVER
    driver.close()
