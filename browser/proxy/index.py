from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }

chrome_options = Options()
# chrome_options.add_experimental_option('w3c', False)

driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
driver.get('https://www.iyf.tv/movie')
logs = driver.get_log('performance')

# 只保留图片相关的请求
image_requests = []
count = 0

for entry in logs:
    log = json.loads(entry['message'])['message']
    if 'Network.requestWillBeSent' in log['method']: # and 'image' in log['params']['type']:
        if log['params'].get('type') == 'Image':
            # print(log['params'].get('request').get('url'))
            # obj = json.loads(json.dumps({}))
            # obj['url'] = log['params'].get('request').get('url')
            image_requests.append(log['params'].get('request').get('url'))
            count += 1
        if count > 200:
            break

# with open('index.json', 'w') as outfile:
#     json.dump(logs, outfile)

with open('image.json', 'w') as outfile:
    json.dump(image_requests, outfile)

driver.close()