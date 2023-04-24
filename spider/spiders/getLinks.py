import scrapy
from w3lib.html import remove_tags
from browser.proxy.index import get_renderer_page, get_m3u8_link
import time

# 这个就做成 www.iyf.tv 专用的
# scrapy crawl getLinks -o quotes.jsonlines
class LinkSpider(scrapy.Spider):
    name = 'getLinks'

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

        # 这里是解析列表页的所有信息，但是是不完整的，所以我们在下面请求具体页面
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
            if element.get('movie_addr') is not None:
                add_params = {}
                add_params['movie_name'] = element.get('movie_name')
                add_params['movie_type'] = element.get('movie_type')
                add_params['movie_mark'] = element.get('movie_mark')
                add_params['movie_poster'] = element.get('movie_poster')

                yield scrapy.Request(
                    url="https://www.iyf.tv" + element.get('movie_addr'),
                    callback=self.get_m3u8_link,
                    cb_kwargs=add_params
                )


    def get_m3u8_link(self, response, movie_name, movie_type, movie_mark, movie_poster):
        # 获取渲染后的页面
        rendered_page = get_renderer_page(response.url)

        # 将渲染后的页面传递给 Scrapy 的 TextResponse 对象
        rendered_response = scrapy.http.TextResponse(url=response.url, body=rendered_page, encoding='utf-8')

        __m3u8_link__ = get_m3u8_link(url=response.url)

        yield {
            "movie_name": movie_name,
            "movie_type": movie_type,
            "movie_addr": __m3u8_link__,
            "movie_time": rendered_response.css('.created.d-flex.ng-star-inserted > span:nth-child(2)::text').get(),
            "movie_mark": movie_mark,
            "movie_actor": remove_tags(rendered_response.css('.d-inline-flex.actors.ng-star-inserted').extract_first()),
            "movie_poster": movie_poster,
        }
