import scrapy
import json
import csv

class RBTeamsSpider(scrapy.Spider):
    name = "rb_shops"

    start_urls = [
        "https://www.redbullshop.com/en-id/c/rb-leipzig/?fq=%3Arelevance&page=0&show=All",
        "https://www.redbullshop.com/en-id/c/rb-racing/?fq=%3Arelevance&page=0&show=All"
    ]

    item_link = set()
    item_datas = dict()
    item_count = 0

    def parse(self, response):
        # Get team name from parameter
        team = response.url.split('/')[-2]

        # self.log(response.url + '' + team)
        yield response.follow(response.url, callback=self.parse_details, meta={'team': team}, dont_filter=True)

        next_page = response.css('button.plp__btn--load-more.btn.btn-outline-secondary.js-plp__btn--load-more::attr(data-page)').get()
        full_next_page = f"https://www.redbullshop.com/en-id/c/{team}/?fq=%3Arelevance&page={next_page}&show=All"
        
        if next_page is not None:
            yield response.follow(full_next_page, callback=self.parse)
            

    def parse_details(self, response):
        for products in response.css("div#plp__grid div.col-sm-6.col-md-4.col-lg-3"):
            try:
                # self.log(products)
                team = response.meta['team']

                other_data = products.css('div.tile__body')
                name = other_data.css(".tile__name::text").get()
                status = other_data.css(".marker::text").get()
                if status is None:
                    status = "Normal"
                else:
                    status = status.strip().capitalize()

                gender = other_data.css(".tile__gender::text").get()
                price = other_data.css(".tile__price--main::text").get().replace('€', '')
                image = products.css("img.tile__image.intrinsic__item::attr(data-src)").get()
                link = "https://www.redbullshop.com" + products.css("a::attr(href)").get()
                
                self.item_count += 1
                self.log(f"{self.item_count} - {team} - {name}")

                if link not in self.item_link:
                    self.item_link.add(link)
                    yield {
                        'name': name,
                        'status': status,
                        'gender': gender,
                        'price': price,
                        'image': image,
                        'link': link,
                        'team': team
                    }

                    # if team not in self.items_datas:
                    #     self.item_datas[team] = []

                    # self.item_datas[team].append(item_data)
                    
                    # with open(f'../{team}.json', 'w', encoding='utf-8') as f:
                    #     json.dump(self.item_datas[team], f, ensure_ascii=False, indent=4)

                    
            except:
                pass






