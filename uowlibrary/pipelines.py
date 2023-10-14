# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from time import time
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import psycopg2 
from re import search

class UowlibraryPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get('title')!= None:
            adapter = ItemAdapter(item)
            
            for image_url in adapter['image_urls']:
                yield Request(image_url,meta={'title':item['title'],'author':item['author']})
            
    def file_path(self, request, response=None, info=None, *, item=None):
        return f"full/{request.meta['title']} by {request.meta['author']}.jpg"



class toPostgresSQLPipeline:
    def __init__(self):
        
        self.cnn = psycopg2.connect(
            host = 'uowlibrary.cfgr3kbul23x.ap-southeast-2.rds.amazonaws.com',
            user = 'shawn',
            password = 'mlpmlpmlp',
            database = 'uowlibrary')
        self.cur = self.cnn.cursor()
        
        
        # self.cur.execute('''drop table book''')
        # self.cnn.commit()
        self.cur.execute('''
                        create table if not exists book(
                        id           serial  primary key,
                        title        varchar(300),
                        brief        varchar(4000),
                        description  varchar(10000),      
                        author       varchar(50),  
                        rating       varchar(50),  

                        publishDate  varchar(200),    
                        pagesFormat   varchar(100),         
                            
                        image_urls   varchar(200)
                        )''')
        self.cnn.commit()


    def process_item(self, item, spider):
       
        title,brief = self.get_title_subtitle(item.get("title"))
      
        description = item.get('description')
        if brief ==  None:
            brief = description[0]

        description = self.make_one_para(description)
        des = description.replace("show more","")

        rating = item.get('rating')
        rating = self.set_rating(rating)
        # brief = self.select_breif_withoutbr(self.select_breif(descrption))
        
        if len(brief)<170:
            self.cur.execute("""insert into book(
            title,brief,description,author,rating,publishDate,pagesFormat,image_urls) values (%s,%s,%s,%s, %s,%s,%s,%s)""",
            (title,brief,des,item.get('author'),rating,item.get('publishDate'),item.get('pagesFormat'),
            item.get('image_urls')[0]
            ))
            self.cnn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.cnn.close()

    def make_one_para(self,ps):
        text = ""
        ps = ps[:-1]
        for p in ps:
                text+=p
                text+="<br>"
        return text
        

    def select_breif(self,description):
        
        brief = description.split(".")[0]
        
        while len(brief)>160:
            if search(",",brief):
                briefs = brief.split(",",20)[:-1]
                brief =""
                for b in briefs:
                        brief+=b
            else:
                break
        brief+="."

        return brief

    def select_breif_withoutbr(self,description):
        brief = description.split(".")[0]
        while len(brief)>160:
            if search("<br>",brief):
                briefs = brief.split("<br>",20)[:-1]
                brief =""
                for b in briefs:
                        brief+=b
            else:
                break
        brief+="."

        brief = brief.replace("<br><br>"," ")

        return brief

    def get_title_subtitle(self,title):
        if ":" in title:           
            return title.split(":")[0],title.split(":")[1]
        else:
            return title,None
    
                  
    def set_rating(self,rating):
        star_count = 0
        if rating == None:
                star_count = 4
        else:
                rating = rating.split(" out")[0]
                star_count = round(float(rating))
        return star_count*'&#9733;'+(5-star_count)*'&#9734;'

    

   
    