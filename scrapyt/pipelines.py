# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter

class ScrapytPipeline:
    
    
    def process_item(self, item, spider):
        # self.exporter.export_item(item)
        # return item
        pass

    # def close_spider(self,spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()