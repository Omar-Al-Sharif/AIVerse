# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from unidecode import unidecode
import re
from dateutil import parser

class ScrapingmodulePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["title"] = unidecode(adapter["title"][0].strip().replace('\f\n\r\t\v',''))
        adapter["content"] = re.sub(' +',' ',unidecode(adapter["content"][0].strip().replace('\n','')))
        
        adapter["published_time"] = parser.isoparse(adapter["published_time"])
        adapter["modified_time"] = parser.isoparse(adapter["modified_time"])
        
        
        return item
