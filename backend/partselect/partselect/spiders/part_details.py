from typing import Any

import scrapy
from scrapy.loader import ItemLoader

from ..items import PartsItem
from ..pipelines import PartDetailsPipeline


class PartDetailsSpider(scrapy.Spider):
    name = "part_details"
    allowed_domains = ["partselect.com"]
    custom_settings = {"ITEM_PIPELINES": {PartDetailsPipeline: 300}}

    def __init__(
        self,
        partselect_number: str,
        **kwargs: Any,
    ):
        super(PartDetailsSpider, self).__init__(**kwargs)

        self.partselect_number = partselect_number

    def start_requests(self):
        self.url = f"https://www.partselect.com/api/search/?searchterm={self.partselect_number}"

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        is_part_valid = (
            response.css("div.search-result__nsearch.col-lg-10.offset-lg-0").get()
            == None
        )
        if not is_part_valid:
            print(
                f"Part {self.partselect_number} is not found, redirected from: {self.url}, to: {response.url}"
            )
            return

        item = ItemLoader(PartsItem(), response)

        item.add_value("id", self.partselect_number)

        keys_css_map = {
            "manufacturer_part_number": 'span[itemprop="mpn"]::text',
            "manufactured_by": 'span[itemprop="name"]::text',
            "description": 'div[itemprop="description"]::text',
        }
        for key, css in keys_css_map.items():
            item.add_css(key, css)

        youtube_id = response.xpath(
            "//div[@id='PartVideos']/following-sibling::div[1]//div/@data-yt-init"
        ).get()
        youtube_link = (
            None
            if youtube_id is None
            else "https://www.youtube.com/watch?v=" + youtube_id
        )
        item.add_value("part_videos", youtube_link)

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
            item.add_value(
                key, "".join(troubleshooting_selectors.xpath(xpath).extract()).strip()
            )

        yield item.load_item()
