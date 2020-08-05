import scrapy
import json
from datetime import datetime

OUTPUT_FILENAME = 'D:/PyCharm/CodePythyon/Tuoitre/ttre.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

class TuoiTre(scrapy.Spider):
    name = 'TuoiTre'
    allowed_domains = ['tuoitre.vn']
    start_urls = ['https://tuoitre.vn/']
    count = 0
    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'article':
            data = {
                'Links': response.url,
                'Category': response.css('div.menu-category li.menu-li1 a::text').getall(),
                'Title': response.css('h1.article-title::text').get(),
                'Source': response.css('div.author::text').getall(),
                'Time': response.css('div.date-time::text').get(),
                'Sub': response.css('h2.sapo::text').get(),
                'Content': response.css('div.content.fck p::text').getall(),
                'Tags': response.css('meta[property="article:tag"]::attr("content")').getall(),
            }

            with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.count += 1
                self.crawler.stats.set_value('CRAWL COUNT', self.count)

        yield from response.follow_all(css='a[href^="https://tuoitre.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)


