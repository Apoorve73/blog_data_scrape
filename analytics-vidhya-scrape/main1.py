from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import json
import pprint

def get_data(path):

    data = {}

    start = time.time()

    data['blog_archive'] = []

    options = webdriver.ChromeOptions()

    base_url = 'https://www.analyticsvidhya.com/'

    cap = DesiredCapabilities.CHROME

    cap["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(executable_path=path, options=options)
    wait = WebDriverWait(driver, 30)

    driver.get(base_url + "blog-archive/")
    time.sleep(5)

    try:
        try:
             pages = driver.find_element_by_class_name('pagination')
        except Exception as e:
            print(f'number boundary\n{e}')

        try:
            last_page_num = pages.find_elements_by_tag_name('a')[4].text
        except Exception as e:
            print(f'number boundary\n{e}')

        try:
            links = []
            for page in range(int(last_page_num)):
                links.append(f'{base_url}blog-archive/page/{page+1}/')
        except Exception as e:
            print(f'list_links\n{e}')

        if(len(data['blog_archive']) == 0):
            count_links = 0
            try:
                for url in links:
                    driver.get(url)
                    try:
                        i=1
                        topic = driver.find_element_by_xpath(f'//*[@id="cur-page"]/div[1]/div[{i}]/article/h3')
                        while (topic):
                            if (True):
                                #print(topic.text)
                                print(topic.text)
                                topic_url = topic.find_element_by_tag_name('a').get_attribute('href')
                                print(topic_url)
                                data['blog_archive'].append({
                                    'topic': topic.text,
                                    'url': topic_url
                                })
                                #print(data)
                                i += 1
                                topic = driver.find_element_by_xpath('//*[@id="cur-page"]/div[1]/div[{}]/article/h3'.format(i))

                    except Exception as e:
                        print(f'headings\n{e}')
                    else:
                        count_links += 1
                        print(f'{count_links} out of {len(links)} scraped! (*__*)')
                        time.sleep(3)

            except Exception as e:
                print(f'headings\n{e}')

        else:
            print('Links already present')

        count = 0
        for info in data['blog_archive']:
            try:
                    driver.get(info['url'])

                    try:
                        bread_crumb = driver.find_element_by_class_name('maha-crumbs').text
                    except Exception as e:
                        print(f'bread_crumb\n{e}')

                    try:
                        more_info = driver.find_element_by_class_name('meta-info')
                        author = more_info.find_element_by_tag_name('span').text
                        published_on = more_info.find_element_by_tag_name('time').text
                    except Exception as e:
                        print(f'more_info \n {e}')

                    try:
                        info.update({
                            'bread-crumb': bread_crumb,
                            'author' : author,
                            'published-on' : published_on
                        })
                    except Exception as e:
                        print(f'info.update\n{e}')
                    time.sleep(3)
                    count+=1
                    print(f'{count} out of {len(data["blog_archive"])} blogs scraped! :)')

            except Exception as e:
                print(f'get_info\n{e}')
                continue


        with open('data1.json', 'w') as outfile:
            json.dump(data, outfile)

        print("Data Uploaded @data.json!")

    except Exception as e:
        print(f'{e}')


    driver.quit()

get_data('../chromedriver_linux/chromedriver')
