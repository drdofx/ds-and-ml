# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv
from datetime import datetime


class RedbullPipeline:
    def open_spider(self, spider):
        now = datetime.now()
        self.start_time = now.strftime("%H-%M_%d-%m-%Y")

    def process_item(self, item, spider):
        team = item['team']

        with open(f'output/{self.start_time}_{team}.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            row = [
                item['name'],
                item['status'],
                item['gender'],
                item['price'],
                item['image'],
                item['link']
            ]

            writer.writerow(row)

        return item
