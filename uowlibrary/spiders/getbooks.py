import scrapy
from itemloaders import ItemLoader
from uowlibrary.items import UowlibraryItem

class GetbooksSpider(scrapy.Spider):
    name = 'getbooks'
    allowed_domains = ["www.goodreads.com"]
    start_urls = ["https://www.goodreads.com/list/show/1.Best_Books_Ever"]
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls[0]=self.get_url() 

    def parse(self, response):

        books = response.xpath("//tr/td[3]/a")
       
        for book in books:
            link = response.urljoin(book.xpath(".//@href").get()) 
            author = book.xpath(".//div[2]/p[1]/a/text()").get()

            yield scrapy.Request(url=link,callback=self.parse_details)

    def parse_details(self,response):
        loader = ItemLoader(item=UowlibraryItem())

        loader.add_value('title',response.xpath("//h1[@data-testid='bookTitle']/text()").get())
        loader.add_value('description',response.xpath("//div[@data-testid='description']//span/text()").getall())
        loader.add_value('author',response.xpath("//span[@class='ContributorLink__name']/text()").get())
        loader.add_value('rating',response.xpath("//div[@class='RatingStatistics__rating']/text()").get())
        loader.add_value('publishDate',response.xpath("//p[@data-testid='publicationInfo']/text()").get())
        loader.add_value('pagesFormat',response.xpath("//p[@data-testid='pagesFormat']/text()").get())
        loader.add_value('image_urls',response.xpath("//img[@class='ResponsiveImage']/@src").get())
    
        yield loader.load_item()

        # yield {
        #     'title':response.xpath("//div[@class='mobile-book-header']/h1[@class='work-title']/text()").get(),
        #     'description':response.xpath("//div[@class='book-description-content restricted-view']/p[1]/text()").get(),
        #     'author':response.xpath("//div[@class='mobile-book-header']/h2/a/text()").get(),
        #     'rating':response.xpath("//div[@class='mobile-book-header']/ul/li/span[@itemprop='ratingValue']/text()").get(),
        #     'publishDate':response.xpath("//span[@itemprop='datePublished']/text()").get(),
        #     'publiser':response.xpath("//a[@itemprop='publisher']/text()").get(),

        #     "link":response.url
        # }

    
    def get_url(self):
        base_url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"
        f = open("page_number.txt","r")
        page_number = int(f.readlines()[0])
        f.close()
        if page_number == 1:
            crnt_url = base_url
        else:
            crnt_url = base_url+"?page="+str(page_number)

        page_number +=1 
        w = open("page_number.txt","w")
        w.write(str(page_number))
        w.close()
        return crnt_url

    