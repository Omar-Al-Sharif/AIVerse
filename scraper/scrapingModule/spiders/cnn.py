import scrapy
from scrapy.spiders import SitemapSpider
from scrapingModule.items import Article
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CNNSpider(SitemapSpider):
    name = "cnn_spider"
    sitemap_urls = ["https://edition.cnn.com/robots.txt"]
    sitemap_follow = ["sitemaps/index","sitemaps/article"]
    sitemap_rules = [('/[\d]{4}/[\d]{2}/[\d]{2}/[\w-]+/[\w-]+-.*','parse_article'),('/[\w]+/[\w]+/[\w\d-]+/index.html','parse_article')]
    def sitemap_filter(self, entries):
        for entry in entries:
            standard_entry = entry["loc"].lower()
            if "live-news" in standard_entry or "/video" in standard_entry or "/calculator" in standard_entry or "/election" in standard_entry or "/interactive" in standard_entry or "/tv" in standard_entry or "/cnn10" in standard_entry:
                continue
            else:
                yield entry
    
    
    
    def parse_article(self, response):
            
        article_item = Article()
        article_item["url"] = ''.join(response.url),
        article_item["title"] = response.css("div.headline__wrapper h1::text").get(),
        article_item["content"] = ''.join(response.css('div.article__content p::text').getall()),
        article_item["tags"] = [x.strip() for x in response.xpath('.//meta[@name="keywords"]/@content').get().split(',')]
        article_item["published_time"] = response.xpath('.//meta[@property="article:published_time"]/@content').get()
        article_item["modified_time"] = response.xpath('.//meta[@property="article:modified_time"]/@content').get()
        article_item["outlet"] = "cnn"
    
        yield article_item
        
                
class FoxSpiderSpider(SitemapSpider):
    name = "fox_spider"
    sitemap_urls = ["https://www.foxnews.com/robots.txt"]
    
    def sitemap_filter(self, entries):
        for entry in entries:
            standard_entry = entry["loc"].lower()
            if "/video" in standard_entry or "/shows" in standard_entry:
                continue
            else:
                yield entry

    def parse(self, response):
        article_item = Article()
        
        article_item["url"] = ''.join(response.url),
        article_item["title"] = response.css("div h1.headline::text").get(),
        article_item["content"] = ''.join(response.css("div.article-body p::text").getall()),
        article_item["tags"] = response.xpath('.//meta[@name="classification-isa"]/@content').get().split(',')
        article_item["published_time"] = response.xpath('.//meta[@name="dcterms.created"]/@content').get()
        article_item["modified_time"] = response.xpath('.//meta[@name="dcterms.modified"]/@content').get()
        article_item["outlet"] = "fox news"
        
        yield article_item

