import scrapy
from w3lib.html import remove_tags
import subprocess
import re
from browser.proxy.index import get_renderer_page

# scrapy crawl getProxy -o IP.json
# https://www.socks-proxy.net/ 网站的免费可用代理爬取
class getProxy(scrapy.Spider):
    name = "getProxy"
    # 可以直接写一个 start_urls = [] 作用和下面这个函数一样
    def start_requests(self):
        urls = [
            'https://www.socks-proxy.net/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取渲染后的页面
        rendered_page = get_renderer_page(response.url)

        # 将渲染后的页面传递给 Scrapy 的 TextResponse 对象
        rendered_response = scrapy.http.TextResponse(url=response.url, body=rendered_page, encoding='utf-8')

        ip_table_list = rendered_response.css('tr')

        for proxy_item in ip_table_list:
            ip_tag = proxy_item.css('td').extract_first()
            
            if ip_tag is not None:
                _ip_ = remove_tags(proxy_item.css('td').extract_first())
                print("=====================")
                print(_ip_)
                print("=====================")
                if self.isIP(_ip_):
                    if self.test_ip(_ip_):
                        yield {
                            "IP": _ip_,
                            "PORT": remove_tags(proxy_item.css('td:nth-child(2)').extract_first())
                        }

    # 判断 IP 是否可用
    def test_ip(self, ip):
        if subprocess.call(['ping', '-n', '1', '-w', '1000', ip]) == 0:
            return True
        return False

    def isIP(self, str):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(str):
            return True
        else:
            return False