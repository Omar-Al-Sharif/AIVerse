# import scrapy
# from scrapy.spiders import SitemapSpider
# from scrapingModule.items import Article


# class FoxSpiderSpider(SitemapSpider):
#     name = "fox_spider"
#     sitemap_urls = ["https://www.foxnews.com/robots.txt"]
    
#     def sitemap_filter(self, entries):
#         for entry in entries:
#             standard_entry = entry["loc"].lower()
#             if "/video" in standard_entry or "/shows" in standard_entry:
#                 continue
#             else:
#                 yield entry

#     def parse(self, response):
#         article_item = Article()
        
#         article_item["url"] = ''.join(response.url),
#         article_item["title"] = response.css("div h1.headline::text").get(),
#         article_item["content"] = ''.join(response.css("div.article-body p::text").getall()),
#         article_item["tags"] =  response.xpath('.//meta[@name="classification-isa"]/@content').get().split(',')
#         article_item["published_time"] = response.xpath('.//meta[@name="dcterms.created"]/@content').get()
#         article_item["modified_time"] = response.xpath('.//meta[@name="dcterms.modified"]/@content').get()
        
#         yield article_item
