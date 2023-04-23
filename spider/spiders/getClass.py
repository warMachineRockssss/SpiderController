import scrapy
from collections import Counter

class getClass(scrapy.Spider):
    name = 'getClass'

    def start_requests(self):
        urls = ['https://blog.csdn.net/xc_zhou/article/details/107452111']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取所有的class属性
        class_list = response.css("*::attr(class)").getall()
        print(class_list)
        # 统计每个 class 出现的次数
        class_count = Counter(class_list)
        # 输出统计结果
        for class_name, count in class_count.items():
            if count > 2:
                yield {
                    'info': ("Class {} appears {} times".format(class_name, count))
                }