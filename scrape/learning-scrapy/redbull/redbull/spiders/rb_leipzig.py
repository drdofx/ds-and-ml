import scrapy

class RBLeipzigSpider(scrapy.Spider):
    name = "rb_leipzig"

    start_urls = [
        "https://www.redbullshop.com/en-id/c/rb-leipzig/?fq=%3Arelevance&page=0&show=All"
    ]

    item_link = set()

    def parse(self, response):
        for products in response.css("div#plp__grid div.col-sm-6.col-md-4.col-lg-3"):
            
            try:
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
                
                if link not in self.item_link:
                    self.item_link.add(link)
                    yield {
                        'name': name,
                        'status': status,
                        'gender': gender,
                        'price': price,
                        'image': image,
                        'link': link
                    }
            except:
                pass

        next_page = response.css('button.plp__btn--load-more.btn.btn-outline-secondary.js-plp__btn--load-more::attr(data-page)').get()
        full_next_page = f"https://www.redbullshop.com/en-id/c/rb-leipzig/?fq=%3Arelevance&page={next_page}&show=All"
        if next_page is not None:
            yield response.follow(full_next_page, callback=self.parse)

