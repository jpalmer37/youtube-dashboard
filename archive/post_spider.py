from gc import callbacks
import scrapy 

class PostSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        "https://www.zyte.com/blog/page/1/",
        "https://www.zyte.com/blog/page/2/"
        #"https://www.youtube.com/"
    ]

    def parse(self, response):
        for post in response.css('div.oxy-post'):
            yield {
                'title':post.css('a.oxy-post-title::text').get(),
                #print(post.css('a.oxy-post-title::attr(href)').get())
                'author': post.css('div.oxy-post-meta-author.oxy-post-meta-item::text').re(r'By\s([^\t]+)'),
                'date' : post.css('.oxy-post-image-date-overlay::text').get().strip()
            }
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)