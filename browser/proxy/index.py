from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.google.com')

title = browser.title
print(title)
browser.implicitly_wait(0.5)