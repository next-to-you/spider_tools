from selenium import webdriver
import time

def process_request():
    # 实现 通过request获取响应对象
    driver = webdriver.Chrome()

    driver.get('https://www.baidu.com')
    # 注意加延迟

    time.sleep(2)

    html = driver.page_source

    driver.quit()

    print(html)
#
# # 将放回的响应传给spider
#

process_request()