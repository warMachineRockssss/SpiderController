import scrapy
from browser.proxy.index import get_renderer_page
import time


class LinkSpider(scrapy.Spider):
    name = 'getLinks'
    # allowed_domains = ['https://www.iyf.tv']  # 替换成你要爬取的网站域名
    # start_urls = ['https://www.iyf.tv/movie']  # 替换成你要爬取的起始 URL 
    def start_requests(self):
        url = ['https://www.iyf.tv/movie']
        for i in range(1, 100, 1):
            time.sleep(2) # 停顿两秒
            yield scrapy.Request(url=url + '?page=' + i, callback=self.parse)

    def parse(self, response):
        # 获取渲染后的页面
        rendered_page = get_renderer_page(response.url)

        # 将渲染后的页面传递给 Scrapy 的 TextResponse 对象
        rendered_response = scrapy.http.TextResponse(url=response.url, body=rendered_page, encoding='utf-8')

        # 获取当前页面中的所有链接
        links = rendered_response.css('a::attr(href)').extract()

        # 获取当前页面中的所有图片链接
        img_links = rendered_response.css('img::attr(src)').extract()

        # 获取当前页面中的所有视频链接
        video_links = rendered_response.css('video::attr(src)').extract()

        # 将获取到的链接存储到一个字典中
        data = {
            'url': response.url,
            'links': links,
            'img_links': img_links,
            'video_links': video_links,
        }

        # 输出字典数据
        yield data

        # # 递归爬取当前页面中的所有链接
        # for link in links:
        #     yield scrapy.Request(link, callback=self.parse)

        # # 递归爬取当前页面中的所有图片链接
        # for img_link in img_links:
        #     yield scrapy.Request(img_link, callback=self.parse)

        # # 递归爬取当前页面中的所有视频链接
        # for video_link in video_links:
        #     yield scrapy.Request(video_link, callback=self.parse)