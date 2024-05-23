import os
from typing import Any

import scrapy
from scrapy.loader import ItemLoader

from ..items import ModelItem, PartsItem
from ..pipelines import AllModelsPartsPipeline

# scrape all models and their parts from partselect.com
class AllModelsPartsSpider(scrapy.Spider):
    name = "all_models_parts"
    allowed_domains = ["partselect.com"]
    start_urls = [
        "https://www.partselect.com/Dishwasher-Models.htm",
        "https://www.partselect.com/Refrigerator-Models.htm",
    ]
    custom_settings = {"ITEM_PIPELINES": {AllModelsPartsPipeline: 300}}

    items_cnt = 0
    dev_threshold = 3

    def parse(self, response):
        yield from response.follow_all(
            css="ul.nf__links a::attr(href)", callback=self.parse_model
        )

        if int(os.environ.get("DEV", "1")) == 1:
            return

        next_page = response.css("ul.pagination li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    #! copied from models spider
    def parse_model(self, response):
        if int(os.environ.get("DEV", "1")) == 1 and self.items_cnt > self.dev_threshold:
            return
        self.items_cnt += 1

        #! removed check for invalid

        self.model_item = ItemLoader(ModelItem(), response)

        name = response.css("h1.title-main::text").get().split("-")[0].strip()
        self.model_item.add_value("name", name)

        model_number = response.url.split("/")[-2]
        self.model_item.add_value("id", model_number)

        self.model_item.add_value("link", response.url)

        #! modified from models spider
        yield response.follow(
            url=f"https://www.partselect.com/Models/{model_number}/Parts",
            callback=self.parse_model_parts,
        )

    #! copied from models spider
    def parse_model_parts(self, response):
        for response_part in response.css("div.mega-m__part"):
            link_selector = response_part.css("a.bold.mb-1.mega-m__part__name")

            part_link = response.urljoin(link_selector.xpath("@href").get())

            yield response.follow(part_link, callback=self.parse_part_details)

        next_page = response.css("ul.pagination li.next a::attr(href)").get()
        if int(os.environ.get("DEV", "1")) != 1 and next_page is not None:
            yield response.follow(next_page, self.parse_model_parts)

    #! copied from parts_details spider
    def parse_part_details(self, response):
        parts_item = ItemLoader(PartsItem(), response)

        parts_item.add_value("link", response.url)

        keys_css_map = {
            "id": 'span[itemprop="productID"]::text',
            "price": 'span[itemprop="price"] span.js-partPrice::text',
            "name": 'span[itemprop="name"]::text',
            "manufacturer_part_number": 'span[itemprop="mpn"]::text',
            "manufactured_by": 'span[itemprop="name"]::text',
            "description": 'div[itemprop="description"]::text',
        }

        for key, css in keys_css_map.items():
            parts_item.add_css(key, css)

        youtube_id = response.xpath(
            "//div[@id='PartVideos']/following-sibling::div[1]//div/@data-yt-init"
        ).get()
        youtube_link = (
            None
            if youtube_id is None
            else "https://www.youtube.com/watch?v=" + youtube_id
        )
        parts_item.add_value("part_videos", youtube_link)

        troubleshooting_selectors = response.xpath(
            '//div[@id="Troubleshooting"]/following-sibling::div[1]'
        )
        keys_xpath_map = {
            "fixes": "./div[1]/text()",
            "works_with_appliances": "./div[2]/text()",
            "works_with_brands": "./div[3]/text()",
            "part_replaces": "./div[4]/div[2]/text()",
        }

        for key, xpath in keys_xpath_map.items():
            parts_item.add_value(
                key, "".join(troubleshooting_selectors.xpath(xpath).extract()).strip()
            )

        self.model_item.add_value("parts", parts_item.load_item())
        yield self.model_item.load_item()
