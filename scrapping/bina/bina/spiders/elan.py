import scrapy


from ..items import BinaItem

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
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            full_link = response.urljoin(next_page)
            yield scrapy.Request(url=full_link,callback=self.parse)
        


    def parse_link(self, response):
            price= response.xpath("//span[@class='price-val']/text()").get() + response.xpath("//span[@class='price-cur']/text()").get()
            price_per_m = response.xpath("//div[@class='unit-price']/text()").get()
            description = response.xpath("//article/p/text()").get()
            value1 = [response.xpath("//table[@class='parameters']/tr[1]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[1]/td[2]/text()").get()]
            value2 = [response.xpath("//table[@class='parameters']/tr[2]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[2]/td[2]/text()").get()]
            value3 = [response.xpath("//table[@class='parameters']/tr[3]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[3]/td[2]/text()").get()]
            value4 = [response.xpath("//table[@class='parameters']/tr[4]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[4]/td[2]/text()").get()]
            value5 = [response.xpath("//table[@class='parameters']/tr[5]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[5]/td[2]/text()").get()]
            value6 = [response.xpath("//table[@class='parameters']/tr[6]/td[1]/text()").get(),response.xpath("//table[@class='parameters']/tr[6]/td[2]/text()").get()]
            values = [value1,value2,value3,value4,value5,value6]
            i=0
            kateqoriya = ""
            mertebe = ""
            sahe = ""
            otaq_sayi = ""
            kupca = ""
            ipoteka = ""
            while (i<6):
                if(values[i][0] == "Kateqoriya"):
                    kateqoriya = values[i][1]
                elif(values[i][0] == "Mərtəbə"):
                    mertebe = values[i][1]
                elif(values[i][0] == "Sahə"):
                    sahe = values[i][1]
                elif(values[i][0] == "Otaq sayı"):
                    otaq_sayi = values[i][1]
                elif(values[i][0] == "Kupça"):
                    kupca = values[i][1]
                elif(values[i][0] == "İpoteka"):
                    ipoteka = values[i][1]
                i+=1
            
            elanlar = BinaItem()

            elanlar['price'] = price
            elanlar['price_per_m'] = price_per_m
            elanlar['description'] = description
            elanlar['kateqoriya'] = kateqoriya
            elanlar['mertebe'] = mertebe
            elanlar['sahe'] = sahe
            elanlar['otaq_sayi'] = otaq_sayi
            elanlar['kupca'] = kupca
            elanlar['ipoteka'] = ipoteka

            yield elanlar
           
            



            