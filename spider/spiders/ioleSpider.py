# xbyy Spider
import scrapy
from w3lib.html import remove_tags
from browser.proxy.index import get_renderer_page, get_m3u8_link
import time
import re

# scrapy crawl ioleSpider -o test.jsonlines
class LinkSpider(scrapy.Spider):
    name = 'ioleSpider'

    def start_requests(self):
        # 热门视频只有一页2---
        url = 'https://www.iole.tv/vodshow/1-----------.html'
        baseUrl = 'https://xcvods.com/vod-list-1--hits------'
        yield scrapy.Request(url=url, callback=self.parse)
        time.sleep(5)
        for i in range(2, 6, 1):
            time.sleep(25) # 停顿两秒
            yield scrapy.Request(url=baseUrl + str(i) + '---.html', callback=self.parse)

    def parse(self, response):
        # 获取渲染后的页面
        rendered_page = get_renderer_page(response.url)

        # 将渲染后的页面传递给 Scrapy 的 TextResponse 对象
        rendered_response = scrapy.http.TextResponse(url=response.url, body=rendered_page, encoding='utf-8')

        # 获取当前页面中的所有链接
        movie_item_list = rendered_response.css('.macplus-vodlist__bag')

        movie_info_list = []

        # 这里是解析列表页的所有信息，但是是不完整的，所以我们在下面请求具体页面
        for item in movie_item_list:
            _link = item.css('.macplus-vodlist__thumb.lazyload::attr(href)').extract_first()

            try:
                movie_info_list.append({
                    'movie_name': remove_tags(item.css('.title.text-overflow').extract_first()),
                    'movie_type': "",
                    'movie_addr': re.search(r"/([^/.]+)\.", _link).group(1),
                    'movie_time': "",
                    'movie_mark': "",
                    'movie_actor': remove_tags(item.css('.text.text-overflow.text-muted.hidden-xs').extract_first()),
                    'movie_poster': item.css('.macplus-vodlist__thumb.lazyload::attr(data-original)').extract_first()
                })
            except BaseException:
                print('解析出错')

        # 输出字典数据
        for element in movie_info_list:
            if element.get('movie_addr') is not None:
                add_params = {}
                add_params['movie_name'] = element.get('movie_name')
                # add_params['movie_type'] = element.get('movie_type')
                add_params['movie_actor'] = element.get('movie_actor')
                add_params['movie_poster'] = element.get('movie_poster')
                # yield {
                #     'movie_name': element.get('movie_name'),
                #     'movie_addr': element.get('movie_addr'),
                #     'movie_actor': element.get('movie_actor'),
                #     'movie_poster': element.get('movie_poster')
                # }

                yield scrapy.Request(
                    url="https://xcvods.com/" + element.get('movie_addr').replace("detail", "play") + "-src-1-num-1.html",
                    callback=self.get_m3u8_link,
                    cb_kwargs=add_params
                )


    def get_m3u8_link(self, response, movie_name, movie_actor, movie_poster):
        __m3u8_link__ = get_m3u8_link(url=re.sub(r'\?.*','', response.url))

        yield {
            "movie_name": movie_name,
            "movie_type": "电影",
            "movie_addr": __m3u8_link__,
            "movie_time": "",
            "movie_mark": "",
            "movie_actor": movie_actor,
            "movie_poster": movie_poster,
        }
