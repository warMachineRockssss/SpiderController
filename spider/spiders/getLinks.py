import scrapy
from browser.proxy.index import get_renderer_page
import time

# 这个就做成 www.iyf.tv 专用的
class LinkSpider(scrapy.Spider):
    name = 'getLinks'
    # allowed_domains = ['https://www.iyf.tv']  # 替换成你要爬取的网站域名
    # start_urls = ['https://www.iyf.tv/movie']  # 替换成你要爬取的起始 URL 
    def start_requests(self):
        url = 'https://www.iyf.tv/movie?page='
        for i in range(1, 2, 1):
            time.sleep(2) # 停顿两秒
            yield scrapy.Request(url=url + str(i), callback=self.parse)

    def parse(self, response):
        # 获取渲染后的页面
        rendered_page = get_renderer_page(response.url)

        # 将渲染后的页面传递给 Scrapy 的 TextResponse 对象
        rendered_response = scrapy.http.TextResponse(url=response.url, body=rendered_page, encoding='utf-8')

        # 获取当前页面中的所有链接
        movie_item_list = rendered_response.css('.v-c.ng-star-inserted')

        movie_info_list = []

        for item in movie_item_list:
            movie_info_list.append({
                'movie_name': item.css('a::attr(title)').extract_first(),
                'movie_type': item.css('.tag-text.text-light span::text').extract_first(),
                'movie_addr': item.css('a::attr(href)').extract_first(),
                'movie_time': '2023-04-23',
                'movie_mark': item.css('.rating.ng-star-inserted::text').extract_first(),
                'movie_actor': '',
                'movie_poster': item.css('img::attr(src)').extract_first()
            })

        # 输出字典数据
        for element in movie_info_list:
            yield element

        # # 递归爬取当前页面中的所有链接
        # for link in links:
        #     yield scrapy.Request(link, callback=self.parse)

        # # 递归爬取当前页面中的所有图片链接
        # for img_link in img_links:
        #     yield scrapy.Request(img_link, callback=self.parse)

        # # 递归爬取当前页面中的所有视频链接
        # for video_link in video_links:
        #     yield scrapy.Request(video_link, callback=self.parse)