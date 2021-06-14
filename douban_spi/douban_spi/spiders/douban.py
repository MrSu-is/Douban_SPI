import scrapy
from ..items import DoubanSpiItem
from time import sleep
import random
from scrapy_redis.spiders import RedisSpider

class DoubanSpider(RedisSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    #start_urls = ['http://douban.com/']
    redis_key = "douban:start_urls"

    def parse(self, response):
        #for i in range(2):
        #    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        #    a = self.driver.execute_script('document.getElementsByClassName("pn-next")[0].click()')
        #    sleep(random(2))
        
        #print(response.url)
        #print(response.status)
        #print(response.body.decode('utf-8'))
        #title = response.css('.hd > a > span:nth-child(1)::text').extract()
        #content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a > span:nth-child(1)
        #rank = response.xpath('//*[@class = "pic"]/em/text()').extract()
        
        #print(title)

        title = response.xpath('//div[@class = "main-bd"]/h2/a/text()').extract()
        author = response.xpath('//a[@class = "name"]/text()').extract()
        #score = response.xpath('//header[@class = "main-hd"]/span/@title').extract()
        picture = response.xpath('//a[@class = "subject-img"]/img/@src').extract()
        abstract = response.xpath('//div[@class = "short-content"]/text()').extract()
        author_time = response.xpath('//span[@class = "main-meta"]/text()').extract()
        detail_pages = response.xpath('//div[@class = "main-bd"]/h2/a/@href').extract()
        #print(title)
        #print(author)
        #print(score)
        #print(picture)
        #print(abstract)
        #print(author_time)
        print(detail_pages)
        for index,detail_page in enumerate(detail_pages):
            abstract_detail = abstract[index]
            title_detail = title[index]
            author_detail = author[index]
            #score_detail = score[index]
            picture_detail = picture[index]
            author_time_detail = author_time[index]
            yield scrapy.Request(detail_page,callback=self.parse_comment_detail,meta={'abstract_detail':abstract_detail,'title_detail':title_detail,'author_detail':author_detail,'picture_detail':picture_detail,'author_time_detail':author_time_detail,},dont_filter=True)
        next_page = response.xpath('//span[@class = "next"]/a/@href').extract_first()
        base_url = 'https://movie.douban.com'
        #print(response.meta['proxy'])
        if next_page:
            yield scrapy.Request(url = base_url + next_page,callback=self.parse,dont_filter=True)

    def parse_comment_detail(self,response):
        reader = response.xpath('//div[@class = "meta-header"]/a/text()').extract_first()
        reader_time = response.xpath('//div[@class = "meta-header"]/time/text()').extract_first()
        comment = response.xpath('//div[@class = "comment-content"]/span/text()').extract_first()
        print(reader)
        print(reader_time)
        print(comment)
        abstract_detail = response.meta['abstract_detail']
        title_detail = response.meta['title_detail']
        author_detail = response.meta['author_detail']
        #score_detail = response.meta['score_detail']
        picture_detail = response.meta['picture_detail']
        author_time_detail = response.meta['author_time_detail']
        item = DoubanSpiItem()
        item['title_detail'] = title_detail
        item['author_detail'] = author_detail
        item['author_time_detail'] = author_time_detail
        item['abstract_detail'] = abstract_detail
        #item['score_detail'] = score_detail
        item['picture_detail'] = picture_detail
        item['reader'] = reader
        item['reader_time'] = reader_time
        item['comment'] = comment
        
        yield item
        #print(item)
        #print(abstract_detail,score)
        #describe = response.xpath('//*[@property = "v:summary"]/text()').extract_first()
        #pattern = '[a-zA-Z]+'
        #num = re.findall(pattern=pattern,string=describe)
        #print(num)