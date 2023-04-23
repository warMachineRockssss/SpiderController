from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time

# 返回网络请求中的图片链接
def get_images_chrome(url, limit):
    """通过直接访问网络请求的形式，获取对应url页面中的所有图片链接，默认使用Chrome
    测试链接：https://www.iyf.tv/movie
    With the selenium, We can get all picture link by network performance

    Args:
        url: 要请求的网页链接
        limit: 限制返回的链接数量
    Returns:
        由链接构成的数组
    """
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'performance':'ALL' }

    chrome_options = Options()
    # chrome_options.add_experimental_option('w3c', False)

    driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
    driver.get(url)
    logs = driver.get_log('performance')

    # 只保留图片相关的请求
    image_requests = []
    count = limit

    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Network.requestWillBeSent' in log['method']:
            if log['params'].get('type') == 'Image':
                # print(log['params'].get('request').get('url'))
                # obj = json.loads(json.dumps({}))
                # obj['url'] = log['params'].get('request').get('url')
                image_requests.append(log['params'].get('request').get('url'))
                count -= 1
            if count < 0:
                break

    # 保存结果到文件
    # with open('image.json', 'w') as outfile:
    #     json.dump(image_requests, outfile)

    driver.close()

    return image_requests

def get_renderer_page(url):
    """
    使用 selenium， 返回渲染后的页面
    """
    # 创建 Chrome 浏览器对象
    options = Options()
    options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    driver = webdriver.Chrome(options=options)

    # 加载页面
    driver.get(url)

    # 滚动到最低端
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
    time.sleep(1)

    # 获取渲染后的页面内容
    rendered_page = driver.page_source

    # 关闭浏览器
    driver.quit()

    return rendered_page