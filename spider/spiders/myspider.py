import scrapy
from pathlib import Path


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    # 可以直接写一个 start_urls = [] 作用和下面这个函数一样
    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 下面这一段代码是保存文件
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')
        # print("==================================")
        # print(response.css('div'))
        # print("==================================")

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # 构建一个完整的绝对URL
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            # follow支持相对URL，这点与Request不同，甚至可以直接将选择器赋值给它
            # yield response.follow(next_page, callback=self.parse)


# 下面是脚本 quotes是爬虫名，上面定于的 -O是输出并覆盖文件，下面这个是往后加
# scrapy crawl quotes -o quotes.jsonlines