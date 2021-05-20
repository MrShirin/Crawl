import scrapy


class ElanSpider(scrapy.Spider):
    name = 'elan'
    allowed_domains = ['bina.az']
    base_url = 'https://bina.az'
    
    def start_requests(self):
        yield scrapy.Request(url='https://bina.az/alqi-satqi/',callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.41 YaBrowser/21.5.0.579 Yowser/2.5 Safari/537.36'})

    def parse(self, response):
        elanlar = response.xpath("//div[@class='items_list']/div[contains(@class,'items')]")
        

        for elan in elanlar:
            item_link= self.base_url + elan.xpath(".//a[@class='item_link']/@href").get()
            yield scrapy.Request(item_link,callback=self.parse_link, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.41 YaBrowser/21.5.0.579 Yowser/2.5 Safari/537.36'})
        
        next_page = response.xpath("//a[@rel='next']/@href").get("href")
        counter=str(next_page).split("page=")[-1]
        if next_page and int(counter)<=20:
            full_link = response.urljoin(next_page)
            yield scrapy.Request(url=full_link,callback=self.parse) 
        


    def parse_link(self, response):
            price= response.xpath("//span[@class='price-val']/text()").get() + response.xpath("//span[@class='price-cur']/text()").get()
            price_per_m = response.xpath("//div[@class='unit-price']/text()").get()
            description = response.xpath("//article/p/text()").get()
            floor = response.xpath("//table[contains(@class,'parameters')]/tr[2]/td[2]/text()").extract_first()
            area = response.xpath("//table[contains(@class,'parameters')]/tr[3]/td[2]/text()").extract_first()

            yield{
                'Qiymet' : price,
                '1m kvadratina qiymet' : price_per_m,
                'Serh' : description,
                'Mertebe': floor,
                'Sahe' : area,
            }



            