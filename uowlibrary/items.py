# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item,Field
from itemloaders.processors import TakeFirst,MapCompose








class UowlibraryItem(Item):
    image_urls= Field (
      )
    images = Field(
    )
    title = Field(
        output_processor = TakeFirst()
    )
    brief = Field(
    
    )
    description = Field(

    )
    author = Field(
          output_processor = TakeFirst()
    )
    rating = Field(
           
            output_processor = TakeFirst()
    )
    publishDate = Field(
          output_processor = TakeFirst()
    )
    pagesFormat = Field(
          output_processor = TakeFirst()
    )
    